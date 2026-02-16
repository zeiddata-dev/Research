"""
zeid_data_collect.py

Pull configured Island API endpoints and write artifacts to NDJSON/JSONL.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

from zeid_data_island_client import IslandClient, AuthConfig, HttpConfig


def iso_now() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def render_placeholders(obj: Any, ctx: Dict[str, Any]) -> Any:
    """
    Replace strings like "{{logs_start}}" with values from ctx.
    """
    if isinstance(obj, str):
        for k, v in ctx.items():
            obj = obj.replace(f"{{{{{k}}}}}", "" if v is None else str(v))
        return obj
    if isinstance(obj, list):
        return [render_placeholders(x, ctx) for x in obj]
    if isinstance(obj, dict):
        return {k: render_placeholders(v, ctx) for k, v in obj.items()}
    return obj


def ensure_parent(file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def append_jsonl(path: Path, item: Any) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, sort_keys=True))
        f.write("\n")


def collect_list_endpoint(client: IslandClient, ep: Dict[str, Any], out_dir: Path, ctx: Dict[str, Any]) -> Dict[str, Any]:
    path = ep["path"]
    params = render_placeholders(ep.get("params") or {}, ctx)
    item_path = ep.get("item_path")
    output = out_dir / ep["output"]

    # clear existing output
    ensure_parent(output)
    if output.exists():
        output.unlink()

    count = 0
    for item in client.iter_items(path, params=params, item_path=item_path):
        append_jsonl(output, item)
        count += 1

    return {"name": ep["name"], "mode": "list", "path": path, "count": count, "output": str(ep["output"])}


def collect_export_job(client: IslandClient, ep: Dict[str, Any], out_dir: Path, ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generic 3-step export job pattern:
    1) POST job_create_path -> returns job_id
    2) GET job_status_path formatted with job_id until status indicates done
    3) Fetch download URL from job_result_field (supports direct URL download)
    """
    import time
    import requests

    create_path = ep["job_create_path"]
    create_body = render_placeholders(ep.get("job_create_body") or {}, ctx)

    status_path_tpl = ep["job_status_path"]
    result_field = ep.get("job_result_field", "download_url")

    output = out_dir / ep["output"]
    ensure_parent(output)
    if output.exists():
        output.unlink()

    job = client.post_json(create_path, json_body=create_body)
    if not isinstance(job, dict):
        raise RuntimeError(f"Job create response was not a dict: {job}")

    job_id = job.get("job_id") or job.get("id") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"Could not find job id in response: {job}")

    # poll status
    poll_seconds = float(ep.get("poll_seconds", 5))
    max_polls = int(ep.get("max_polls", 120))  # ~10 minutes by default

    status_payload = None
    for _ in range(max_polls):
        status_path = status_path_tpl.format(job_id=job_id)
        status_payload = client.get_json(status_path)
        if isinstance(status_payload, dict):
            status = (status_payload.get("status") or status_payload.get("state") or "").lower()
            if status in ("done", "completed", "complete", "finished", "success"):
                break
            if status in ("failed", "error"):
                raise RuntimeError(f"Export job failed: {status_payload}")
        time.sleep(poll_seconds)

    if not isinstance(status_payload, dict):
        raise RuntimeError(f"Job status response was not a dict: {status_payload}")

    download_url = status_payload.get(result_field)
    if not isinstance(download_url, str) or not download_url.startswith("http"):
        raise RuntimeError(f"Could not find download URL in field '{result_field}'. Response: {status_payload}")

    # Download result (assuming it is either JSONL/NDJSON, JSON, or CSV).
    # Store it as-is; bundle builder will hash it.
    r = requests.get(download_url, timeout=60)
    r.raise_for_status()
    output.write_bytes(r.content)

    return {
        "name": ep["name"],
        "mode": "export_job",
        "job_id": str(job_id),
        "create_path": create_path,
        "status_path": status_path_tpl,
        "output": str(ep["output"]),
        "bytes": output.stat().st_size,
    }


def main() -> int:
    load_dotenv()

    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to zeid_data_config.yaml")
    ap.add_argument("--out", required=True, help="Output directory (collection root)")
    ap.add_argument("--since-hours", type=int, default=None, help="Override logs_start/logs_end with last N hours")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))

    base_url = cfg["base_url"]
    auth_cfg = cfg.get("auth") or {}
    http_cfg = cfg.get("http") or {}

    api_key_env = auth_cfg.get("api_key_env", "ISLAND_API_KEY")
    api_key = os.environ.get(api_key_env, "")

    auth = AuthConfig(
        header=auth_cfg.get("header", "Authorization"),
        prefix=auth_cfg.get("prefix", "Bearer"),
        api_key=api_key,
    )
    http = HttpConfig(
        timeout_seconds=int(http_cfg.get("timeout_seconds", 30)),
        verify_ssl=bool(http_cfg.get("verify_ssl", True)),
        max_retries=int(http_cfg.get("max_retries", 6)),
        backoff_seconds=float(http_cfg.get("backoff_seconds", 1.0)),
    )

    client = IslandClient(base_url=base_url, auth=auth, http=http)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    collection_cfg = cfg.get("collection") or {}
    logs_start = collection_cfg.get("logs_start")
    logs_end = collection_cfg.get("logs_end")

    if args.since_hours is not None:
        end = dt.datetime.utcnow().replace(microsecond=0)
        start = end - dt.timedelta(hours=args.since_hours)
        logs_start = start.isoformat() + "Z"
        logs_end = end.isoformat() + "Z"

    ctx = {
        "logs_start": logs_start,
        "logs_end": logs_end,
    }

    meta = {
        "started_at": iso_now(),
        "base_url": base_url,
        "endpoints": [],
        "errors": [],
    }

    endpoints = cfg.get("endpoints") or []
    for ep in endpoints:
        try:
            mode = ep.get("mode", "list")
            if mode == "list":
                meta["endpoints"].append(collect_list_endpoint(client, ep, out_dir, ctx))
            elif mode == "export_job":
                meta["endpoints"].append(collect_export_job(client, ep, out_dir, ctx))
            else:
                raise RuntimeError(f"Unknown endpoint mode: {mode}")
        except Exception as e:
            meta["errors"].append({"endpoint": ep.get("name"), "error": str(e)})

    meta["finished_at"] = iso_now()
    write_json(out_dir / "collection_metadata.json", meta)

    if meta["errors"]:
        print("Collection completed with errors. See collection_metadata.json.")
        return 2

    print("Collection completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
