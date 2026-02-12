#!/usr/bin/env python3
"""
zeid_data_backup_verify.py

Verifies backup targets by:
- existence
- modified time (age threshold)
- optional minimum file size

Outputs JSON + CSV.
This is not a backup system. It's a lie detector.
"""

from __future__ import annotations

import argparse, csv, json, sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

@dataclass
class BackupCheck:
    target: str
    exists: bool
    is_dir: bool
    mtime_utc: Optional[str]
    age_hours: Optional[float]
    size_bytes: Optional[int]
    ok: bool
    error: Optional[str] = None

def read_targets(path: Path) -> List[str]:
    out: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

def check(t: str, max_age_hours: float, min_size_bytes: int) -> BackupCheck:
    p = Path(t)
    try:
        if not p.exists():
            return BackupCheck(t, False, False, None, None, None, False, "missing")
        st = p.stat()
        is_dir = p.is_dir()
        mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
        age_h = (datetime.now(timezone.utc) - mtime).total_seconds() / 3600.0
        size = None if is_dir else st.st_size
        ok = (age_h <= max_age_hours)
        if (not is_dir) and min_size_bytes > 0 and size is not None and size < min_size_bytes:
            ok = False
        return BackupCheck(t, True, is_dir, mtime.isoformat(), round(age_h, 2), size, ok, None)
    except Exception as ex:
        return BackupCheck(t, False, False, None, None, None, False, str(ex))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--max-age-hours", type=float, default=24.0)
    ap.add_argument("--min-size-bytes", type=int, default=0)
    ap.add_argument("--out-dir", default="out")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: input not found: {inp}", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    targets = read_targets(inp)
    if not targets:
        print("ERROR: no targets provided.", file=sys.stderr)
        return 2

    results = [check(t, args.max_age_hours, args.min_size_bytes) for t in targets]
    (out_dir / "backup_verify.json").write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    with (out_dir / "backup_verify.csv").open("w", newline="", encoding="utf-8") as f:
        wri = csv.DictWriter(f, fieldnames=["target","exists","is_dir","mtime_utc","age_hours","size_bytes","ok","error"])
        wri.writeheader()
        for r in results:
            wri.writerow(asdict(r))

    ok = sum(1 for r in results if r.ok)
    print(f"OK: {ok}/{len(results)}. Outputs in: {out_dir.resolve()}")
    return 0 if ok == len(results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
