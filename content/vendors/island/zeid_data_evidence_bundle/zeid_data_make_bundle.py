"""
zeid_data_make_bundle.py

Build a tamper-evident evidence bundle:
- copies collected artifacts into a bundle folder
- generates SHA256 for every file
- writes manifest.json + chain_of_custody.md + reports/summary.md
- zips the bundle for distribution
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


TOOL_NAME = "zeid-data-island-evidence-bundle-kit"
TOOL_VERSION = "0.1.0"


def iso_now() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def guess_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in (".json", ".jsonl", ".ndjson"):
        return "application/json"
    if ext in (".csv",):
        return "text/csv"
    if ext in (".md", ".txt"):
        return "text/plain"
    if ext in (".yaml", ".yml"):
        return "text/yaml"
    return "application/octet-stream"


def canonicalize_json(obj: Any) -> str:
    # stable ordering for hashing comparisons
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def load_jsonl(path: Path) -> List[Any]:
    out: List[Any] = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


def summarize_collection(collection_dir: Path) -> Dict[str, Any]:
    meta_path = collection_dir / "collection_metadata.json"
    meta = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    data_dir = collection_dir / "data"
    counts = {}
    if data_dir.exists():
        for p in sorted(data_dir.glob("*")):
            if p.is_file():
                # count lines for jsonl
                if p.suffix.lower() in (".jsonl", ".ndjson"):
                    counts[p.name] = sum(1 for _ in p.open("r", encoding="utf-8"))
                else:
                    counts[p.name] = p.stat().st_size
    return {"metadata": meta, "counts": counts}


def compare_policy_drift(baseline_dir: Path, current_dir: Path) -> Dict[str, Any]:
    """
    Best-effort drift compare for policies.jsonl if present.
    """
    baseline = baseline_dir / "data" / "island_policies.jsonl"
    current = current_dir / "data" / "island_policies.jsonl"

    if not baseline.exists() or not current.exists():
        return {"available": False, "reason": "Missing island_policies.jsonl in baseline or current."}

    base_items = load_jsonl(baseline)
    curr_items = load_jsonl(current)

    # build stable identity keys
    def ident(x: Any) -> str:
        if isinstance(x, dict):
            for k in ("id", "policy_id", "policyId", "uuid", "name"):
                if k in x and isinstance(x[k], (str, int)):
                    return str(x[k])
        return hashlib.sha256(canonicalize_json(x).encode("utf-8")).hexdigest()

    base_map = {ident(x): hashlib.sha256(canonicalize_json(x).encode("utf-8")).hexdigest() for x in base_items}
    curr_map = {ident(x): hashlib.sha256(canonicalize_json(x).encode("utf-8")).hexdigest() for x in curr_items}

    added = sorted([k for k in curr_map.keys() if k not in base_map])
    removed = sorted([k for k in base_map.keys() if k not in curr_map])
    changed = sorted([k for k in curr_map.keys() if k in base_map and curr_map[k] != base_map[k]])

    return {
        "available": True,
        "baseline_count": len(base_items),
        "current_count": len(curr_items),
        "added": added[:200],
        "removed": removed[:200],
        "changed": changed[:200],
        "note": "Identity matching is best-effort; adjust ident() if your policy objects have better keys.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_dir", required=True, help="Collection directory (output of zeid_data_collect.py)")
    ap.add_argument("--out", dest="out_dir", required=True, help="Output directory for bundles")
    ap.add_argument("--case-id", required=True, help="Case identifier (ticket, matter, audit ID)")
    ap.add_argument("--custodian", required=True, help="Name of evidence custodian")
    ap.add_argument("--baseline", default=None, help="Optional baseline collection dir for drift compare")
    args = ap.parse_args()

    collection_dir = Path(args.in_dir)
    if not collection_dir.exists():
        raise SystemExit(f"Collection dir not found: {collection_dir}")

    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    ts = dt.datetime.utcnow().replace(microsecond=0).strftime("%Y%m%dT%H%M%SZ")
    bundle_id = f"{args.case_id}_{ts}"
    bundle_dir = out_root / f"evidence_bundle_{bundle_id}"
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Copy raw artifacts
    for name in ("collection_metadata.json", "data"):
        src = collection_dir / name
        if src.exists():
            dst = bundle_dir / name
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

    # Reports
    reports_dir = bundle_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_collection(collection_dir)
    summary_md = [
        f"# Evidence Bundle Summary",
        "",
        f"- Bundle ID: `{bundle_id}`",
        f"- Case ID: `{args.case_id}`",
        f"- Created (UTC): `{iso_now()}`",
        "",
        "## Collected counts",
        "",
    ]
    for k, v in summary["counts"].items():
        summary_md.append(f"- `{k}`: `{v}`")
    summary_md.append("")
    (reports_dir / "summary.md").write_text("\n".join(summary_md), encoding="utf-8")

    drift_info = None
    if args.baseline:
        drift = compare_policy_drift(Path(args.baseline), collection_dir)
        drift_info = drift
        drift_md = ["# Policy drift (best-effort)", ""]
        if not drift.get("available"):
            drift_md.append(f"Drift compare not available: {drift.get('reason')}")
        else:
            drift_md += [
                f"- Baseline policies: `{drift['baseline_count']}`",
                f"- Current policies: `{drift['current_count']}`",
                f"- Added: `{len(drift['added'])}`",
                f"- Removed: `{len(drift['removed'])}`",
                f"- Changed: `{len(drift['changed'])}`",
                "",
                "## Sample keys (first 200 max per bucket)",
                "",
                "### Added",
                "```",
                *drift["added"],
                "```",
                "### Removed",
                "```",
                *drift["removed"],
                "```",
                "### Changed",
                "```",
                *drift["changed"],
                "```",
                "",
                f"Note: {drift.get('note')}",
            ]
        (reports_dir / "policy_drift.md").write_text("\n".join(drift_md), encoding="utf-8")

    # Chain of custody
    coc = [
        "# Chain of custody",
        "",
        f"- Case ID: {args.case_id}",
        f"- Bundle ID: {bundle_id}",
        f"- Custodian: {args.custodian}",
        f"- Created (UTC): {iso_now()}",
        "",
        "## Handling notes",
        "- Collection artifacts were copied from the provided collection directory.",
        "- File integrity is represented by SHA256 hashes recorded in manifest.json.",
        "- Preserve this bundle as read-only once produced.",
        "",
        "## Collection metadata",
    ]
    meta_path = bundle_dir / "collection_metadata.json"
    if meta_path.exists():
        coc.append("```json")
        coc.append(meta_path.read_text(encoding="utf-8"))
        coc.append("```")
    (bundle_dir / "chain_of_custody.md").write_text("\n".join(coc), encoding="utf-8")

    # Manifest with hashes
    files = []
    for p in sorted(bundle_dir.rglob("*")):
        if p.is_file():
            rel = p.relative_to(bundle_dir).as_posix()
            files.append({
                "path": rel,
                "sha256": sha256_file(p),
                "bytes": p.stat().st_size,
                "content_type_guess": guess_content_type(p),
            })

    base_url = None
    if meta_path.exists():
        try:
            base_url = json.loads(meta_path.read_text(encoding="utf-8")).get("base_url")
        except Exception:
            base_url = None

    manifest = {
        "bundle_id": bundle_id,
        "created_at": iso_now(),
        "case_id": args.case_id,
        "custodian": args.custodian,
        "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
        "source": {
            "base_url": base_url or "",
            "collection_metadata": "collection_metadata.json",
            "notes": "See chain_of_custody.md for context.",
        },
        "files": files,
    }
    (bundle_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    # Zip it
    zip_path = out_root / f"evidence_bundle_{bundle_id}.zip"
    if zip_path.exists():
        zip_path.unlink()

    import zipfile
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(bundle_dir.rglob("*")):
            if p.is_file():
                z.write(p, arcname=p.relative_to(bundle_dir).as_posix())

    print(f"Wrote: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
