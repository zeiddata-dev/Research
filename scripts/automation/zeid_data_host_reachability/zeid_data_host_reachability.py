#!/usr/bin/env python3
"""
zeid_data_host_reachability.py

Reads a list of hosts/IPs and checks basic ICMP reachability via the system `ping`.
Outputs CSV + JSON. Because "it works on my machine" isn't evidence.

Notes:
- Uses your OS ping binary (no raw sockets).
- Use on systems you own/manage or have explicit permission to test.
"""

from __future__ import annotations

import argparse
import csv
import json
import platform
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any

@dataclass
class Result:
    host: str
    reachable: bool
    packet_loss_pct: Optional[float] = None
    avg_rtt_ms: Optional[float] = None
    raw_hint: Optional[str] = None

PING_RE_WIN_LOSS = re.compile(r"Lost\s*=\s*(\d+)\s*\((\d+)%\s*loss\)", re.IGNORECASE)
PING_RE_WIN_AVG  = re.compile(r"Average\s*=\s*(\d+)\s*ms", re.IGNORECASE)
PING_RE_NIX_LOSS = re.compile(r"(\d+(?:\.\d+)?)%\s*packet\s*loss", re.IGNORECASE)
PING_RE_NIX_RTT  = re.compile(r"(?:rtt|round-trip).*=\s*[\d\.]+/([\d\.]+)/", re.IGNORECASE)

def read_hosts(path: Path) -> List[str]:
    hosts: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        hosts.append(line)
    return hosts

def run_ping(host: str, count: int, timeout_ms: int) -> subprocess.CompletedProcess:
    system = platform.system().lower()
    if "windows" in system:
        cmd = ["ping", "-n", str(count), "-w", str(timeout_ms), host]
    else:
        timeout_s = max(1, int(round(timeout_ms / 1000)))
        cmd = ["ping", "-c", str(count), "-W", str(timeout_s), host]
    return subprocess.run(cmd, capture_output=True, text=True)

def parse_ping_output(output: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"packet_loss_pct": None, "avg_rtt_ms": None}
    m = PING_RE_WIN_LOSS.search(output)
    if m: out["packet_loss_pct"] = float(m.group(2))
    m = PING_RE_WIN_AVG.search(output)
    if m: out["avg_rtt_ms"] = float(m.group(1))
    m = PING_RE_NIX_LOSS.search(output)
    if m and out["packet_loss_pct"] is None: out["packet_loss_pct"] = float(m.group(1))
    m = PING_RE_NIX_RTT.search(output)
    if m and out["avg_rtt_ms"] is None: out["avg_rtt_ms"] = float(m.group(1))
    return out

def main() -> int:
    ap = argparse.ArgumentParser(description="Check reachability for hosts via system ping.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--count", type=int, default=2)
    ap.add_argument("--timeout-ms", type=int, default=1500)
    ap.add_argument("--out-dir", default="out")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: input file not found: {inp}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    hosts = read_hosts(inp)
    if not hosts:
        print("ERROR: no hosts found. Provide at least one non-comment line.", file=sys.stderr)
        return 2

    results: List[Result] = []
    for host in hosts:
        proc = run_ping(host, args.count, args.timeout_ms)
        combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        reachable = (proc.returncode == 0)
        parsed = parse_ping_output(combined)
        hint = None
        if parsed["packet_loss_pct"] is None and parsed["avg_rtt_ms"] is None:
            hint = (combined[:200] + "…") if len(combined) > 200 else combined
        results.append(Result(host, reachable, parsed["packet_loss_pct"], parsed["avg_rtt_ms"], hint))

    (out_dir / "reachability.json").write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    with (out_dir / "reachability.csv").open("w", newline="", encoding="utf-8") as f:
        wri = csv.DictWriter(f, fieldnames=["host","reachable","packet_loss_pct","avg_rtt_ms","raw_hint"])
        wri.writeheader()
        for r in results:
            wri.writerow(asdict(r))

    ok = sum(1 for r in results if r.reachable)
    print(f"Reachable: {ok}/{len(results)}. Evidence in: {out_dir.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
