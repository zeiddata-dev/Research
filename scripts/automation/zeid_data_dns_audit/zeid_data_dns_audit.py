#!/usr/bin/env python3
"""
zeid_data_dns_audit.py

Resolves hostnames to A/AAAA using the system resolver (socket.getaddrinfo).
Outputs CSV + JSON for evidence, because DNS loves being "fine" right up until it isn't.
"""

from __future__ import annotations

import argparse, csv, json, socket, sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Set

@dataclass
class DnsResult:
    name: str
    ok: bool
    a_records: List[str]
    aaaa_records: List[str]
    error: Optional[str] = None

def read_names(path: Path) -> List[str]:
    out: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

def resolve(name: str) -> DnsResult:
    a: Set[str] = set()
    aaaa: Set[str] = set()
    try:
        infos = socket.getaddrinfo(name, None)
        for fam, _, _, _, sa in infos:
            if fam == socket.AF_INET: a.add(sa[0])
            elif fam == socket.AF_INET6: aaaa.add(sa[0])
        return DnsResult(name, True, sorted(a), sorted(aaaa))
    except Exception as ex:
        return DnsResult(name, False, [], [], str(ex))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", default="out")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: input not found: {inp}", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    names = read_names(inp)
    if not names:
        print("ERROR: no names provided. DNS can't resolve emptiness.", file=sys.stderr)
        return 2

    results = [resolve(n) for n in names]
    (out_dir / "dns_audit.json").write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")

    with (out_dir / "dns_audit.csv").open("w", newline="", encoding="utf-8") as f:
        wri = csv.DictWriter(f, fieldnames=["name","ok","a_records","aaaa_records","error"])
        wri.writeheader()
        for r in results:
            wri.writerow({
                "name": r.name,
                "ok": r.ok,
                "a_records": " ".join(r.a_records),
                "aaaa_records": " ".join(r.aaaa_records),
                "error": r.error or ""
            })

    ok = sum(1 for r in results if r.ok)
    print(f"Resolved: {ok}/{len(results)}. Outputs in: {out_dir.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
