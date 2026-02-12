#!/usr/bin/env python3
"""
zeid_data_route_snapshot.py

Captures the current route table to a timestamped file and optionally diffs against the previous snapshot.

Because "nothing changed" in networking is comedy.
"""

from __future__ import annotations

import argparse, datetime as dt, platform, subprocess
from pathlib import Path
from typing import List

def run_cmd(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()

def get_routes() -> str:
    sysname = platform.system().lower()
    if "windows" in sysname:
        return run_cmd(["route", "print"])
    try:
        out = run_cmd(["ip", "route"])
        if out:
            return out
    except Exception:
        pass
    return run_cmd(["netstat", "-rn"])

def unified_diff(a: str, b: str) -> str:
    import difflib
    return "".join(difflib.unified_diff(
        a.splitlines(keepends=True),
        b.splitlines(keepends=True),
        fromfile="previous",
        tofile="current",
    ))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--diff", action="store_true")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    current = get_routes()

    snap = out_dir / f"routes_{now}.txt"
    snap.write_text(current + "\n", encoding="utf-8")
    print(f"Wrote snapshot: {snap.resolve()}")

    if args.diff:
        snaps = sorted(out_dir.glob("routes_*.txt"))
        if len(snaps) < 2:
            print("No previous snapshot to diff. Congratulations on starting evidence collection today.")
            return 0
        prev = snaps[-2].read_text(encoding="utf-8", errors="replace")
        diff = unified_diff(prev, current)
        diff_path = out_dir / f"routes_diff_{now}.patch"
        diff_path.write_text(diff if diff else "# No differences. Calm. Suspicious.\n", encoding="utf-8")
        print(f"Wrote diff: {diff_path.resolve()}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
