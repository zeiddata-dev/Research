#!/usr/bin/env python3

"""
zeid_data_inventory_python.py
Authorized network inventory helper.

- Passive: parse ARP/neighbor cache
- Optional active: ping sweep (opt-in)
- Optional reverse DNS
- Output: JSONL or CSV
"""

import argparse, ipaddress, platform, subprocess, socket, csv, json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def run_cmd(cmd, timeout=5):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    except Exception:
        return ""

def is_ipv4(s):
    try:
        ipaddress.IPv4Address(s); return True
    except Exception:
        return False

def is_mac(s):
    parts = s.split(":")
    if len(parts) != 6: return False
    try:
        return all(len(p)==2 and int(p,16)>=0 for p in parts)
    except Exception:
        return False

def parse_neighbors():
    sys = platform.system().lower()
    recs = {}
    if "windows" in sys:
        out = run_cmd(["arp","-a"])
        for line in out.splitlines():
            line = line.strip()
            if not line or line.lower().startswith("interface:") or line.lower().startswith("internet address"):
                continue
            parts = [p for p in line.split() if p]
            if len(parts) >= 2 and is_ipv4(parts[0]):
                ip = parts[0]
                mac = parts[1].replace("-",":").lower()
                if is_mac(mac):
                    recs[ip] = {"ip": ip, "mac": mac, "seen_via": "arp"}
    else:
        out = run_cmd(["ip","neigh"])
        if out.strip():
            for line in out.splitlines():
                parts = line.split()
                if len(parts) < 2 or not is_ipv4(parts[0]): continue
                ip = parts[0]
                mac = None
                if "lladdr" in parts:
                    idx = parts.index("lladdr")
                    if idx+1 < len(parts): mac = parts[idx+1].lower()
                if mac and is_mac(mac):
                    recs[ip] = {"ip": ip, "mac": mac, "seen_via": "neigh"}
                else:
                    recs.setdefault(ip, {"ip": ip, "mac": None, "seen_via": "neigh"})
        else:
            out2 = run_cmd(["arp","-an"])
            import re
            for line in out2.splitlines():
                m = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:]{17})", line, re.I)
                if m:
                    ip, mac = m.group(1), m.group(2).lower()
                    recs[ip] = {"ip": ip, "mac": mac, "seen_via": "arp"}
    return recs

def ping_host(ip, timeout_ms):
    sys = platform.system().lower()
    if "windows" in sys:
        cmd = ["ping","-n","1","-w",str(timeout_ms), ip]
    else:
        sec = max(1, int(round(timeout_ms/1000)))
        cmd = ["ping","-c","1","-W",str(sec), ip]
    try:
        p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return p.returncode == 0
    except Exception:
        return False

def rev_dns(ip, timeout_sec=2):
    try:
        socket.setdefaulttimeout(timeout_sec)
        host,_,_ = socket.gethostbyaddr(ip)
        return host
    except Exception:
        return None

def iter_hosts(subnet):
    net = ipaddress.ip_network(subnet, strict=False)
    hosts = list(net.hosts())
    if len(hosts) > 4096:
        raise SystemExit(f"Refusing to scan {len(hosts)} hosts; use a smaller subnet.")
    for ip in hosts:
        yield str(ip)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subnet", help="IPv4 CIDR (e.g., 192.168.1.0/24). Required for --active.")
    ap.add_argument("--active", action="store_true", help="Opt-in ping sweep across --subnet")
    ap.add_argument("--timeout-ms", type=int, default=750)
    ap.add_argument("--workers", type=int, default=64)
    ap.add_argument("--dns", action="store_true", help="Best-effort reverse DNS")
    ap.add_argument("--out", default="inventory.jsonl")
    ap.add_argument("--format", choices=["jsonl","csv"], default="jsonl")
    args = ap.parse_args()

    records = parse_neighbors()
    reachable = {}

    if args.active:
        if not args.subnet:
            raise SystemExit("ERROR: --active requires --subnet (e.g., 192.168.1.0/24)")
        hosts = list(iter_hosts(args.subnet))
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(ping_host, ip, args.timeout_ms): ip for ip in hosts}
            for fut in as_completed(futs):
                ip = futs[fut]
                ok = False
                try: ok = bool(fut.result())
                except Exception: ok = False
                reachable[ip] = ok
                if ok and ip not in records:
                    records[ip] = {"ip": ip, "mac": None, "seen_via": "ping"}

        # refresh neighbor cache after ping
        post = parse_neighbors()
        for ip, rec in post.items():
            if ip not in records:
                records[ip] = rec
            else:
                if not records[ip].get("mac") and rec.get("mac"):
                    records[ip]["mac"] = rec.get("mac")
                if records[ip].get("seen_via") == "ping":
                    records[ip]["seen_via"] = rec.get("seen_via") or "neighbor"

    if args.dns:
        for ip in list(records.keys()):
            h = rev_dns(ip)
            if h:
                records[ip]["hostname"] = h

    ts = now_iso()
    rows = []
    for ip in sorted(records.keys(), key=lambda s: tuple(int(x) for x in s.split("."))):
        rec = records[ip]
        rows.append({
            "ip": ip,
            "mac": rec.get("mac"),
            "hostname": rec.get("hostname"),
            "reachable": reachable.get(ip) if args.active else None,
            "seen_via": rec.get("seen_via"),
            "timestamp": ts
        })

    if args.format == "jsonl":
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    else:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            w = csv.DictWriter(f, fieldnames=["ip","mac","hostname","reachable","seen_via","timestamp"])
            w.writeheader()
            w.writerows(rows)

    print(f"Wrote {len(rows)} record(s) to {args.out}")

if __name__ == "__main__":
    main()
