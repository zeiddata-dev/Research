#!/usr/bin/env python3
"""
generate_coverage_report.py
Map evidence files to controls and produce a simple markdown report.

Assumptions:
- evidence is a folder already unpacked (or a curated folder)
- evidence files contain control ids in their file names OR inside a README

Usage:
  python scripts/generate_coverage_report.py --controls controls/zeid_data_control_matrix.csv --evidence out/unpacked_demo --output out/control_coverage.md
"""
import argparse
import csv
from pathlib import Path
import re

CONTROL_ID_RE = re.compile(r"(ZD-AI-[A-Z]+-\d{2})")

def load_controls(path: Path):
    controls = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            controls.append(row)
    return controls

def find_mentions(evidence_dir: Path):
    mentions = {}
    for p in evidence_dir.rglob("*"):
        if p.is_dir():
            continue
        text = ""
        try:
            if p.suffix.lower() in [".md", ".txt", ".csv", ".json", ".jsonl", ".yml", ".yaml", ".conf"]:
                text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            text = ""

        hits = set(CONTROL_ID_RE.findall(p.name)) | set(CONTROL_ID_RE.findall(text))
        for cid in hits:
            mentions.setdefault(cid, []).append(p.relative_to(evidence_dir).as_posix())
    return mentions

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    controls_path = Path(args.controls)
    evidence_dir = Path(args.evidence)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    controls = load_controls(controls_path)
    mentions = find_mentions(evidence_dir)

    covered = 0
    lines = []
    lines.append("# AI Control Coverage Report\n")
    lines.append(f"- Controls file: `{controls_path}`")
    lines.append(f"- Evidence dir: `{evidence_dir}`\n")
    lines.append("| Control ID | Function | Domain | Covered | Evidence files |")
    lines.append("|---|---|---|---|---|")

    for c in controls:
        cid = c["control_id"]
        ev = mentions.get(cid, [])
        is_cov = "Yes" if ev else "No"
        if ev:
            covered += 1
        lines.append(f"| {cid} | {c['function']} | {c['domain']} | {is_cov} | {', '.join(ev) if ev else ''} |")

    lines.append("\n## Summary\n")
    lines.append(f"- Total controls: {len(controls)}")
    lines.append(f"- Covered: {covered}")
    lines.append(f"- Uncovered: {len(controls) - covered}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
