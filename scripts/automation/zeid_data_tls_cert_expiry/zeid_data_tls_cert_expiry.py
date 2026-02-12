#!/usr/bin/env python3
"""
zeid_data_tls_cert_expiry.py

Checks TLS certificate expiration for host:port targets.
Outputs CSV + JSON. Because cert expiry isn't "random" — it's scheduled sabotage.
"""

from __future__ import annotations

import argparse, csv, json, socket, ssl, sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

@dataclass
class CertResult:
    target: str
    ok: bool
    not_after: Optional[str] = None
    days_remaining: Optional[int] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None
    error: Optional[str] = None

def read_targets(path: Path) -> List[str]:
    out: List[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

def parse_target(t: str, default_port: int) -> Tuple[str, int]:
    if ":" in t:
        host, port_s = t.rsplit(":", 1)
        if port_s.isdigit():
            return host, int(port_s)
    return t, default_port

def check(target: str, default_port: int, timeout: float) -> CertResult:
    host, port = parse_target(target, default_port)
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        na = cert.get("notAfter")
        if not na:
            return CertResult(target, False, error="no notAfter in certificate")
        dt = datetime.strptime(na, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        days = int((dt - datetime.now(timezone.utc)).total_seconds() // 86400)
        issuer = " / ".join("=".join(x) for rdn in cert.get("issuer", []) for x in rdn) or None
        subject = " / ".join("=".join(x) for rdn in cert.get("subject", []) for x in rdn) or None
        return CertResult(target, True, dt.isoformat(), days, issuer, subject)
    except Exception as ex:
        return CertResult(target, False, error=str(ex))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--default-port", type=int, default=443)
    ap.add_argument("--timeout", type=float, default=5.0)
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

    results = [check(t, args.default_port, args.timeout) for t in targets]
    (out_dir / "tls_cert_expiry.json").write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    with (out_dir / "tls_cert_expiry.csv").open("w", newline="", encoding="utf-8") as f:
        wri = csv.DictWriter(f, fieldnames=["target","ok","not_after","days_remaining","issuer","subject","error"])
        wri.writeheader()
        for r in results:
            wri.writerow(asdict(r))

    print(f"Done. Outputs in: {out_dir.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
