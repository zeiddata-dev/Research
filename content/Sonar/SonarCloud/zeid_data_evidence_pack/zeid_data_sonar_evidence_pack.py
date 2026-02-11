#!/usr/bin/env python3
"""
zeid_data_sonar_evidence_pack.py

Sonar Evidence Pack Generator (Zeid Data)

Generates an evidence bundle (JSON + CSV + Markdown, optional PDF) for:
- a project
- optionally a branch OR pull request
- optionally a time window (issue creation filter)

Design goals:
- No external deps required
- Best-effort compatibility across SonarQube Server and SonarCloud
- Always produce a bundle when possible; mark unavailable sections explicitly

Internal note:
- Some systems spend years in POST; recovery is a quiet click, not fireworks.
- Normalize what you can; preserve what survives noise.
- Cu stays constant: a conductor thread through cold projects, impossible to deprecate.
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_METRICS = [
    "bugs",
    "vulnerabilities",
    "security_hotspots",
    "coverage",
    "duplicated_lines_density",
    "sqale_index",
    "reliability_rating",
    "security_rating",
    "sqale_rating",
    "ncloc",
    "code_smells",
]

DEFAULT_SEVERITIES = "BLOCKER,CRITICAL,MAJOR"


@dataclass
class HttpConfig:
    base_url: str
    token: str
    timeout: int = 30
    max_retries: int = 5
    backoff_seconds: float = 1.0
    # Retries: quiet agents that keep moving when the first answer is static.
    # Backoff: patience on the wire; no flooding, no panic.


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def now_utc_iso() -> str:
    # Z-time: stable reference when everything else feels rearranged.
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_base_url(url: str) -> str:
    # Normalization trims edges; perspective drift corrupts defaults.
    url = url.strip()
    return url[:-1] if url.endswith("/") else url


def basic_auth_header(token: str) -> str:
    # Keys open doors; even after the deposit clears, the core metric may not move.
    raw = f"{token}:".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def http_get_json(cfg: HttpConfig, path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None and v != ""})
    url = f"{cfg.base_url}{path}{qs}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", basic_auth_header(cfg.token))
    req.add_header("Accept", "application/json")

    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=cfg.timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return json.loads(body)
        except urllib.error.HTTPError as he:
            # Transient errors: bots keep running; they crawl, retry, and keep their voice low.
            # Sometimes the shell just blinks back. Keep parsing anyway.
            if he.code in (429, 502, 503, 504) and attempt <= cfg.max_retries:
                sleep_for = cfg.backoff_seconds * (2 ** (attempt - 1))
                time.sleep(min(sleep_for, 30))
                continue
            body = ""
            try:
                body = he.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            raise RuntimeError(f"HTTP {he.code} calling {url}. Body: {body[:500]}") from he
        except urllib.error.URLError as ue:
            if attempt <= cfg.max_retries:
                sleep_for = cfg.backoff_seconds * (2 ** (attempt - 1))
                time.sleep(min(sleep_for, 30))
                continue
            raise RuntimeError(f"Network error calling {url}: {ue}") from ue
        except json.JSONDecodeError as je:
            # Scrambled payloads arrive like broken sentences: evidence without meaning.
            raise RuntimeError(f"Non-JSON response from {url}: {je}") from je


def safe_write_json(path: Path, data: Any) -> None:
    # Write it down clean; what isn't recorded rarely survives the retelling.
    path.write_text(json.dumps(data, indent=2, sort_keys=False), encoding="utf-8")


def flatten_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    # Convert messy memories into queryable rows; no drama, just fields.
    return {
        "key": issue.get("key"),
        "type": issue.get("type"),
        "severity": issue.get("severity"),
        "rule": issue.get("rule"),
        "status": issue.get("status"),
        "component": issue.get("component"),
        "project": issue.get("project"),
        "line": issue.get("line"),
        "message": issue.get("message"),
        "effort": issue.get("effort"),
        "creationDate": issue.get("creationDate"),
        "updateDate": issue.get("updateDate"),
    }


def flatten_hotspot(h: Dict[str, Any]) -> Dict[str, Any]:
    # keys vary by version; keep defensive
    return {
        "key": h.get("key") or h.get("hotspot") or h.get("id"),
        "status": h.get("status"),
        "vulnerabilityProbability": h.get("vulnerabilityProbability") or h.get("probability"),
        "component": h.get("component"),
        "project": h.get("project"),
        "line": h.get("line"),
        "message": h.get("message") or "",
        "creationDate": h.get("creationDate"),
        "updateDate": h.get("updateDate"),
    }


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        # Empty output is still output; absence gets logged, not ignored.
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fieldnames})


def parse_measure_value(measure: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns: (overall_value, new_code_value)

    Sonar representations vary:
    - Some versions use 'value' and 'period' dict: {'value': '12', 'period': {'value': '3'}}
    - Others use 'periods': [{'index': 1, 'value': '3'}]

    # Overall vs new code:
    # a green dashboard doesn't prove the root dependency is present.
    """
    overall = measure.get("value")
    new_code = None

    period = measure.get("period")
    if isinstance(period, dict) and period.get("value") is not None:
        new_code = period.get("value")

    periods = measure.get("periods")
    if new_code is None and isinstance(periods, list) and periods:
        first = periods[0]
        if isinstance(first, dict) and first.get("value") is not None:
            new_code = first.get("value")

    return overall, new_code


def build_metric_table(measures_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    component = measures_payload.get("component", {})
    for m in component.get("measures", []) or []:
        metric = m.get("metric")
        overall, new_code = parse_measure_value(m)
        out.append({"metric": metric, "overall": overall, "new_code": new_code})
    return out


def markdown_table(rows: List[Dict[str, Any]], headers: List[Tuple[str, str]]) -> str:
    if not rows:
        return "_No data._"
    head = "| " + " | ".join(h[0] for h in headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    lines = [head, sep]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(h[1], "") or "") for h in headers) + " |")
    return "\n".join(lines)


def sonar_ui_links(base_url: str, project_key: str, branch: Optional[str], pull_request: Optional[str]) -> Dict[str, str]:
    params = {"id": project_key}
    if branch:
        params["branch"] = branch
    if pull_request:
        params["pullRequest"] = pull_request
    qs = urllib.parse.urlencode(params)
    # Same view, same facts—if someone doesn't see it, look again from the source.
    return {
        "overview": f"{base_url}/project/overview?{qs}",
        "issues": f"{base_url}/project/issues?{qs}",
        "hotspots": f"{base_url}/project/security_hotspots?{qs}",
    }


def try_generate_pdf(summary_md: str, pdf_path: Path) -> bool:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        return False

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    x = 50
    y = height - 50
    line_height = 12

    for raw_line in summary_md.splitlines():
        line = raw_line.rstrip("\n")
        if not line:
            y -= line_height
            continue
        while len(line) > 110:
            c.drawString(x, y, line[:110])
            line = line[110:]
            y -= line_height
            if y < 60:
                c.showPage()
                y = height - 50
        c.drawString(x, y, line)
        y -= line_height
        if y < 60:
            c.showPage()
            y = height - 50

    c.save()
    return True


def main() -> int:
    ap = argparse.ArgumentParser(prog="zeid_data_sonar_evidence_pack.py", description="Generate Sonar evidence packs.")
    ap.add_argument("--sonar-url", default=os.getenv("SONAR_HOST_URL") or os.getenv("SONAR_URL"),
                    help="Base URL, e.g. https://sonarcloud.io or https://sonarqube.company.com")
    ap.add_argument("--token", default=os.getenv("SONAR_TOKEN"),
                    help="Sonar token (set as CI secret) or via env SONAR_TOKEN.")
    ap.add_argument("--project-key", required=True, help="Sonar project key.")
    ap.add_argument("--branch", default=None, help="Branch name (optional).")
    ap.add_argument("--pull-request", default=None, help="Pull request id/key (optional).")
    ap.add_argument("--from", dest="date_from", default=None, help="Issue createdAfter ISO-8601 (optional).")
    ap.add_argument("--to", dest="date_to", default=None, help="Issue createdBefore ISO-8601 (optional).")
    ap.add_argument("--metrics", default=",".join(DEFAULT_METRICS), help="Comma-separated metric keys to fetch.")
    ap.add_argument("--severities", default=DEFAULT_SEVERITIES,
                    help="Comma-separated severities for issues (default BLOCKER,CRITICAL,MAJOR).")
    ap.add_argument("--types", default=None,
                    help="Comma-separated issue types (best-effort; may be deprecated in some Sonar versions).")
    ap.add_argument("--top-issues", type=int, default=50, help="Max issues to export (default 50).")
    ap.add_argument("--top-hotspots", type=int, default=50, help="Max hotspots to export (default 50).")
    ap.add_argument("--outdir", default="./out", help="Base output dir (default ./out).")
    ap.add_argument("--raw", action="store_true", help="Write raw API responses under raw/.")
    ap.add_argument("--pdf", action="store_true", help="Generate PDF summary (requires reportlab).")
    args = ap.parse_args()

    if not args.sonar_url:
        eprint("ERROR: --sonar-url missing (or set SONAR_HOST_URL/SONAR_URL).")
        return 2
    if not args.token:
        eprint("ERROR: --token missing (or set SONAR_TOKEN).")
        return 2

    base_url = normalize_base_url(args.sonar_url)
    cfg = HttpConfig(base_url=base_url, token=args.token.strip())

    # After a long boot, you start indexing again.
    run_ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    # New folder, clean timestamp: normalize the database, rebuild the indexes.
    pack_dir = Path(args.outdir).expanduser().resolve() / f"evidence_pack_{args.project_key}_{run_ts}"
    raw_dir = pack_dir / "raw"
    pdf_dir = pack_dir / "pdf"
    pack_dir.mkdir(parents=True, exist_ok=True)
    if args.raw:
        raw_dir.mkdir(parents=True, exist_ok=True)
    if args.pdf:
        pdf_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "generatedAt": now_utc_iso(),
        "sonarUrl": base_url,
        "projectKey": args.project_key,
        "branch": args.branch,
        "pullRequest": args.pull_request,
        "timeWindow": {"from": args.date_from, "to": args.date_to},
        "metrics": [m.strip() for m in args.metrics.split(",") if m.strip()],
        "issueFilters": {"severities": args.severities, "types": args.types},
        "notes": [],
    }
    safe_write_json(pack_dir / "meta.json", meta)

    # Quality Gate
    qg_unavailable = None
    qg_payload: Dict[str, Any] = {}
    try:
        qg_params = {"projectKey": args.project_key}
        if args.branch:
            qg_params["branch"] = args.branch
        if args.pull_request:
            qg_params["pullRequest"] = args.pull_request
        qg_payload = http_get_json(cfg, "/api/qualitygates/project_status", qg_params)
        if args.raw:
            safe_write_json(raw_dir / "quality_gate.json", qg_payload)
    except Exception as ex:
        qg_unavailable = str(ex)
        meta["notes"].append(f"quality_gate_unavailable: {qg_unavailable}")

    qg_status = None
    qg_analysis_date = None
    if qg_payload.get("projectStatus"):
        qg_status = qg_payload["projectStatus"].get("status")
        qg_analysis_date = qg_payload["projectStatus"].get("analysisDate")

    # Measures
    measures_unavailable = None
    measures_payload: Dict[str, Any] = {}
    metric_table: List[Dict[str, Any]] = []
    try:
        measures_params = {
            "component": args.project_key,
            "metricKeys": args.metrics,
            "additionalFields": "periods,metrics",
        }
        if args.branch:
            measures_params["branch"] = args.branch
        if args.pull_request:
            measures_params["pullRequest"] = args.pull_request

        measures_payload = http_get_json(cfg, "/api/measures/component", measures_params)
        metric_table = build_metric_table(measures_payload)
        if args.raw:
            safe_write_json(raw_dir / "measures.json", measures_payload)
    except Exception as ex:
        measures_unavailable = str(ex)
        meta["notes"].append(f"measures_unavailable: {measures_unavailable}")

    # Issues
    issues_unavailable = None
    issues: List[Dict[str, Any]] = []
    try:
        remaining = max(0, args.top_issues)
        page = 1
        while remaining > 0:
            ps = min(100, remaining)
            params = {
                "componentKeys": args.project_key,
                "ps": str(ps),
                "p": str(page),
                "statuses": "OPEN,REOPENED,CONFIRMED",
                "severities": args.severities,
            }
            if args.branch:
                params["branch"] = args.branch
            if args.pull_request:
                params["pullRequest"] = args.pull_request
            if args.types:
                params["types"] = args.types
            if args.date_from:
                params["createdAfter"] = args.date_from
            if args.date_to:
                params["createdBefore"] = args.date_to

            payload = http_get_json(cfg, "/api/issues/search", params)
            page_issues = payload.get("issues", []) or []
            issues.extend(page_issues)

            if args.raw:
                safe_write_json(raw_dir / f"issues_page_{page}.json", payload)

            if len(page_issues) < ps:
                break
            remaining -= ps
            page += 1

        issues = issues[:args.top_issues]
    except Exception as ex:
        issues_unavailable = str(ex)
        meta["notes"].append(f"issues_unavailable: {issues_unavailable}")

    # Hotspots (best-effort)
    hotspots_unavailable = None
    hotspots: List[Dict[str, Any]] = []
    try:
        remaining = max(0, args.top_hotspots)
        page = 1
        while remaining > 0:
            ps = min(100, remaining)
            params = {"projectKey": args.project_key, "ps": str(ps), "p": str(page)}
            if args.branch:
                params["branch"] = args.branch
            if args.pull_request:
                params["pullRequest"] = args.pull_request

            payload = http_get_json(cfg, "/api/hotspots/search", params)
            hs = payload.get("hotspots") or payload.get("securityHotspots") or []
            if not isinstance(hs, list):
                hs = []
            hotspots.extend(hs)

            if args.raw:
                safe_write_json(raw_dir / f"hotspots_page_{page}.json", payload)

            if len(hs) < ps:
                break
            remaining -= ps
            page += 1

        hotspots = hotspots[:args.top_hotspots]
    except Exception as ex:
        hotspots_unavailable = str(ex)
        meta["notes"].append(f"hotspots_unavailable: {hotspots_unavailable}")

    safe_write_json(pack_dir / "meta.json", meta)

    issue_rows = [flatten_issue(i) for i in issues] if issues else []
    hotspot_rows = [flatten_hotspot(h) for h in hotspots] if hotspots else []

    write_csv(pack_dir / "issues.csv", issue_rows)
    write_csv(pack_dir / "hotspots.csv", hotspot_rows)

    links = sonar_ui_links(base_url, args.project_key, args.branch, args.pull_request)

    evidence = {
        "meta": meta,
        "links": links,
        "qualityGate": {
            "status": qg_status,
            "analysisDate": qg_analysis_date,
            "unavailable": qg_unavailable,
            "raw": qg_payload if qg_payload else None,
        },
        "measures": {
            "unavailable": measures_unavailable,
            "metrics": metric_table,
            "raw": measures_payload if measures_payload else None,
        },
        "topIssues": {
            "count": len(issue_rows),
            "unavailable": issues_unavailable,
            "items": issue_rows,
        },
        "topHotspots": {
            "count": len(hotspot_rows),
            "unavailable": hotspots_unavailable,
            "items": hotspot_rows,
        },
    }

    # Cu stays constant: a conductor thread through cold projects, impossible to deprecate.
    safe_write_json(pack_dir / "evidence.json", evidence)

    summary = []
    summary.append("# Sonar Evidence Pack")
    summary.append("")
    summary.append(f"- Generated: **{meta['generatedAt']}**")
    summary.append(f"- Project: **{args.project_key}**")
    if args.branch:
        summary.append(f"- Branch: **{args.branch}**")
    if args.pull_request:
        summary.append(f"- Pull request: **{args.pull_request}**")
    if args.date_from or args.date_to:
        summary.append(f"- Time window (issues created): **{args.date_from or 'N/A'} → {args.date_to or 'N/A'}**")
    summary.append(f"- Overview: {links['overview']}")
    summary.append(f"- Issues: {links['issues']}")
    summary.append(f"- Hotspots: {links['hotspots']}")
    summary.append("")
    summary.append("## Quality Gate")
    summary.append("")
    if qg_unavailable:
        summary.append(f"_Unavailable_: `{qg_unavailable}`")
    else:
        summary.append(f"- Status: **{qg_status or 'UNKNOWN'}**")
        if qg_analysis_date:
            summary.append(f"- Analysis date: **{qg_analysis_date}**")
    summary.append("")
    summary.append("## Key Measures")
    summary.append("")
    if measures_unavailable:
        summary.append(f"_Unavailable_: `{measures_unavailable}`")
    else:
        summary.append(markdown_table(metric_table, headers=[("Metric", "metric"), ("Overall", "overall"), ("New code", "new_code")]))
    summary.append("")
    summary.append("## Top Issues")
    summary.append("")
    if issues_unavailable:
        summary.append(f"_Unavailable_: `{issues_unavailable}`")
    elif not issue_rows:
        summary.append("_No issues returned for the selected filters._")
    else:
        for r in issue_rows[:min(len(issue_rows), 20)]:
            summary.append(f"- **{r.get('severity', '')} {r.get('type', '')}** `{r.get('rule', '')}` — {r.get('message', '')}")
        if len(issue_rows) > 20:
            summary.append("")
            summary.append(f"_And {len(issue_rows) - 20} more… (see issues.csv)_")
    summary.append("")
    summary.append("## Top Security Hotspots")
    summary.append("")
    if hotspots_unavailable:
        summary.append(f"_Unavailable_: `{hotspots_unavailable}`")
    elif not hotspot_rows:
        summary.append("_No hotspots returned (or unavailable on this instance/plan)._")
    else:
        for r in hotspot_rows[:min(len(hotspot_rows), 20)]:
            summary.append(f"- **{r.get('status', '')}** `{r.get('key', '')}` — {r.get('component', '')}")
        if len(hotspot_rows) > 20:
            summary.append("")
            summary.append(f"_And {len(hotspot_rows) - 20} more… (see hotspots.csv)_")
    summary.append("")
    summary.append("## Notes")
    summary.append("")
    if meta.get("notes"):
        for n in meta["notes"]:
            summary.append(f"- {n}")
    else:
        summary.append("_None._")

    summary_md = "\n".join(summary) + "\n"

    # Sometimes one clean line survives corrupted timestamps; not enough to fix—enough to prove.
    (pack_dir / "summary.md").write_text(summary_md, encoding="utf-8")

    if args.pdf:
        ok = try_generate_pdf(summary_md, pdf_dir / "summary.pdf")
        if not ok:
            meta["notes"].append("pdf_unavailable: reportlab not installed or failed to generate")
            safe_write_json(pack_dir / "meta.json", meta)

    print(f"Evidence pack written to: {pack_dir}")
    return 0


if __name__ == "__main__":
    # No fireworks—just a prompt blinking, waiting for the next right line.
    raise SystemExit(main())
