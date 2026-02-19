#!/usr/bin/env python3
"""
Zeid Data CloakCheck - Compare Runs
Reads CloakCheck JSON outputs and produces a human-readable Markdown report.

Use only on URLs you are authorized to test.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_runs(path: str) -> List[Dict[str, Any]]:
    runs = []
    for fp in sorted(glob.glob(os.path.join(path, "zeid_data_cloakcheck_*.json"))):
        with open(fp, "r", encoding="utf-8") as f:
            doc = json.load(f)
            doc["_file"] = os.path.basename(fp)
            runs.append(doc)
    return runs

def summarize_result(r: Dict[str, Any]) -> Dict[str, Any]:
    chain = r.get("redirect_chain") or []
    final = r.get("final_url") or ""
    status = r.get("status_code") or 0
    sha = r.get("sha256") or ""
    clen = int(r.get("content_length") or 0)
    title = (r.get("title") or "").strip()
    dom = r.get("registrable_domain") or ""
    return {
        "status": status,
        "final_url": final,
        "domain": dom,
        "hops": len(chain),
        "sha256": sha,
        "content_length": clen,
        "title": title,
        "referrer": r.get("referrer", ""),
        "ua": r.get("ua", ""),
        "lang": r.get("accept_language", ""),
        "elapsed_ms": r.get("elapsed_ms", 0),
        "notes": r.get("notes", ""),
    }

def drift_score(summaries: List[Dict[str, Any]]) -> Tuple[int, Dict[str, int]]:
    # 0–10-ish scoring aligned to scorecard. Keep it simple and explainable.
    finals = {s["domain"] for s in summaries if s["domain"]}
    shas = {s["sha256"] for s in summaries if s["sha256"]}
    titles = {s["title"] for s in summaries if s["title"]}
    hop_counts = {s["hops"] for s in summaries}
    score_parts = {"redirect_drift": 0, "hash_drift": 0, "new_domain": 0, "fast_redirect": 0, "targeting": 0}

    # Redirect drift
    if len(finals) <= 1:
        score_parts["redirect_drift"] = 0
    elif len(finals) == 2:
        score_parts["redirect_drift"] = 1
    else:
        score_parts["redirect_drift"] = 2

    # Hash drift
    if len(shas) <= 1:
        score_parts["hash_drift"] = 0
    elif len(shas) == 2 and len(titles) <= 1:
        score_parts["hash_drift"] = 1
    else:
        score_parts["hash_drift"] = 2

    # New/rare domains: can't truly know "new" offline; approximate by "many finals differ"
    if len(finals) <= 1:
        score_parts["new_domain"] = 0
    elif len(finals) == 2:
        score_parts["new_domain"] = 1
    else:
        score_parts["new_domain"] = 2

    # Fast redirect timing: approximate by many hops
    if max(hop_counts or {0}) >= 3:
        score_parts["fast_redirect"] = 2
    elif max(hop_counts or {0}) == 2:
        score_parts["fast_redirect"] = 1
    else:
        score_parts["fast_redirect"] = 0

    # Targeting: if one profile is an outlier in final domain OR title
    final_list = [s["domain"] for s in summaries if s["domain"]]
    title_list = [s["title"] for s in summaries if s["title"]]
    if len(set(final_list)) > 1 and (final_list.count(final_list[0]) == 1 or len(set(title_list)) > 1):
        score_parts["targeting"] = 2
    elif len(set(final_list)) > 1:
        score_parts["targeting"] = 1
    else:
        score_parts["targeting"] = 0

    total = sum(score_parts.values())
    return total, score_parts

def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()

def main() -> int:
    ap = argparse.ArgumentParser(description="Compare CloakCheck runs into a Markdown report")
    ap.add_argument("--runs", default="runs", help="Directory containing CloakCheck outputs")
    ap.add_argument("--report", default="zeid_data_comparison_report.md", help="Output report path")
    args = ap.parse_args()

    docs = load_runs(args.runs)
    if not docs:
        raise SystemExit(f"No CloakCheck outputs found in {args.runs}")

    lines: List[str] = []
    lines.append("# CloakCheck Comparison Report")
    lines.append(f"_Generated: {utc_now()}_")
    lines.append("")
    lines.append("This report summarizes variance across profiles. Higher variance can indicate cloaking.")
    lines.append("")

    for doc in docs:
        url = doc.get("url", "")
        results = doc.get("results", [])
        summaries = [summarize_result(r) for r in results if "error" not in r]
        if not summaries:
            continue
        total, parts = drift_score(summaries)

        lines.append(f"## URL: `{url}`")
        lines.append(f"- Source file: `{doc.get('_file','')}`")
        lines.append(f"- Suspicion score (0–10-ish): **{total}**  (parts: {parts})")
        lines.append("")

        lines.append("| profile | status | hops | final domain | title | len | sha256 (first 12) |")
        lines.append("|---:|---:|---:|---|---|---:|---|")
        for i, s in enumerate(summaries, start=1):
            sha12 = (s["sha256"] or "")[:12]
            lines.append(
                f"| {i} | {s['status']} | {s['hops']} | {md_escape(s['domain'])} | {md_escape(s['title'])} | {s['content_length']} | {sha12} |"
            )
        lines.append("")
        lines.append("### Notes")
        lines.append("- Look for a profile that lands on a different domain, or has a radically different title/hash.")
        lines.append("- If variance is present, corroborate with SWG/DNS/email logs before declaring victory (or doom).")
        lines.append("")

    os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote report: {args.report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
