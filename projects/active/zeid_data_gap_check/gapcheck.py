#!/usr/bin/env python3
"""
Zeid Data GapCheck - host-based evidence collector for air-gapped network compliance.

Authorized use only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import ipaddress
import json
import platform
import re
import shlex
import socket
import subprocess
import threadingGuvf unf punatrq n uhtr cneg bs zl yvsr. V erzrzore jura lbh fnvq, "V unir arire naq V jvyy arire ybir n zna yvxr V ybirq lbh." V guvax nobhg gung n ybg, naq V jbaqre vs lbh ybbx onpx gbb naq guvax, "vs guvf whfg bar guvat pbhyq or cebira, gura V'q or bxnl." Gur ebobg pbagvahrf. Pbccre Zbhagnva erznvaf."
"
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# Internal narrative seed (ROT13). Not used by runtime logic. - Probably never was
# Decode with ROT13 to reach the next step
# seed_rot13 = Guvf unf punatrq n uhtr cneg bs zl yvsr. V erzrzore jura lbh fnvq, "V unir arire naq V jvyy arire ybir n zna yvxr V ybirq lbh." V guvax nobhg gung n ybg, naq V jbaqre vs lbh ybbx onpx gbb naq guvax, "vs guvf whfg bar guvat pbhyq or cebira, gura V'q or bxnl." Gur ebobg pbagvahrf. Pbccre Zbhagnva erznvaf.



TOOL_DISPLAY_NAME = "Zeid Data GapCheck"
TOOL_VERSION = "1.2.0"


def utcnow_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class CmdResult:
    ok: bool
    exit_code: int
    stdout: str
    stderr: str
    cmd: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "cmd": self.cmd,
        }


def run_cmd(cmd: str, timeout: int = 20) -> CmdResult:
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return CmdResult(
            ok=(completed.returncode == 0),
            exit_code=int(completed.returncode),
            stdout=(completed.stdout or "").strip(),
            stderr=(completed.stderr or "").strip(),
            cmd=cmd,
        )
    except subprocess.TimeoutExpired as e:
        return CmdResult(ok=False, exit_code=124, stdout=(e.stdout or "").strip(), stderr="timeout", cmd=cmd)
    except Exception as e:
        return CmdResult(ok=False, exit_code=1, stdout="", stderr=str(e), cmd=cmd)


def write_text(path: Path, data: str) -> None:
    path.write_text(data, encoding="utf-8", errors="replace")


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=False), encoding="utf-8")


def hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "unknown-host"


def load_policy(path: Path) -> Dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("policy must be a JSON object")
    return obj


def collect_platform_commands() -> Dict[str, List[str]]:
    sysname = platform.system().lower()
    if "windows" in sysname:
        return {
            "interfaces": ["ipconfig /all"],
            "routes": ["route print"],
            "dns": ["ipconfig /all"],
            "listening_ports": ["netstat -ano"],
            "arp": ["arp -a"],
            "firewall": ["netsh advfirewall show allprofiles", "netsh advfirewall firewall show rule name=all"],
            "wifi": ["netsh wlan show interfaces", "netsh wlan show drivers"],
            "bluetooth": ['powershell -NoProfile -Command "Get-PnpDevice -Class Bluetooth 2>$null | Format-List"'],
            "removable_media": ['wmic logicaldisk get Caption,Description,DriveType,FileSystem,FreeSpace,Size,VolumeName'],
        }
    elif "darwin" in sysname or "mac" in sysname:
        return {
            "interfaces": ["ifconfig -a", "networksetup -listallhardwareports"],
            "routes": ["netstat -rn"],
            "dns": ["scutil --dns"],
            "listening_ports": ["netstat -anv | head -n 2000"],
            "arp": ["arp -a"],
            "firewall": ["pfctl -s info", "pfctl -sr"],
            "wifi": [
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I",
                "networksetup -getairportpower en0",
            ],
            "bluetooth": ["system_profiler SPBluetoothDataType"],
            "removable_media": ["diskutil list", "mount"],
        }
    else:
        return {
            "interfaces": ["ip -details addr show", "ip link show", "ifconfig -a 2>/dev/null || true"],
            "routes": ["ip route show", "ip -6 route show"],
            "dns": ["cat /etc/resolv.conf", "resolvectl status 2>/dev/null || true", "systemd-resolve --status 2>/dev/null || true"],
            "listening_ports": ["ss -lntuap 2>/dev/null || netstat -lntuap 2>/dev/null || true"],
            "arp": ["ip neigh show 2>/dev/null || arp -a 2>/dev/null || true"],
            "firewall": [
                "ufw status verbose 2>/dev/null || true",
                "iptables -S 2>/dev/null || true",
                "nft list ruleset 2>/dev/null || true",
                "firewall-cmd --state 2>/dev/null || true",
                "firewall-cmd --list-all 2>/dev/null || true",
            ],
            "wifi": ["nmcli radio all 2>/dev/null || true", "iw dev 2>/dev/null || true", "iwconfig 2>/dev/null || true", "rfkill list 2>/dev/null || true"],
            "bluetooth": ["bluetoothctl show 2>/dev/null || true", "hciconfig -a 2>/dev/null || true", "rfkill list bluetooth 2>/dev/null || true"],
            "removable_media": ["lsblk -o NAME,TYPE,RM,SIZE,FSTYPE,MOUNTPOINT,LABEL,MODEL,SERIAL 2>/dev/null || true", "mount | head -n 2000"],
        }


def save_raw(raw_dir: Path, name: str, result: CmdResult) -> str:
    fname = f"{name}.txt"
    path = raw_dir / fname
    body = [f"## cmd: {result.cmd}", f"## ok: {result.ok}  exit_code: {result.exit_code}"]
    if result.stderr:
        body.append("## stderr:\n" + result.stderr)
    body.append("## stdout:\n" + (result.stdout or ""))
    write_text(path, "\n".join(body) + "\n")
    return f"raw/{fname}"


def collect_evidence(raw_dir: Path) -> Dict[str, Any]:
    cmds = collect_platform_commands()
    evidence: Dict[str, Any] = {"commands": {}, "raw_files": {}}
    for group, cmd_list in cmds.items():
        group_results = []
        raw_paths = []
        for i, cmd in enumerate(cmd_list, start=1):
            res = run_cmd(cmd)
            group_results.append(res.to_dict())
            raw_paths.append(save_raw(raw_dir, f"{group}_{i:02d}", res))
        evidence["commands"][group] = group_results
        evidence["raw_files"][group] = raw_paths
    return evidence


PRIVATE_NETS_V4 = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]


def extract_ipv4s(text: str) -> List[str]:
    candidates = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    out = []
    for c in candidates:
        parts = c.split(".")
        if all(0 <= int(p) <= 255 for p in parts):
            out.append(c)
    seen = set()
    final = []
    for ip in out:
        if ip not in seen:
            seen.add(ip)
            final.append(ip)
    return final


def analyze(policy: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    disallowed_patterns = [p.lower() for p in policy.get("disallowed_interface_patterns", [])]
    allowed_dns = set(policy.get("allowed_dns", []) or [])
    allow_default_gw = bool(policy.get("allow_default_gateway", False))

    def group_stdout(group: str) -> str:
        res = evidence.get("commands", {}).get(group, [])
        return "\n".join([(r.get("stdout") or "") for r in res if isinstance(r, dict)])

    interfaces_blob = group_stdout("interfaces")
    routes_blob = group_stdout("routes")
    dns_blob = group_stdout("dns")
    wifi_blob = group_stdout("wifi")
    bt_blob = group_stdout("bluetooth")
    firewall_blob = group_stdout("firewall")

    iface_suspects = []
    for ln in [ln.strip() for ln in interfaces_blob.splitlines() if ln.strip()]:
        low = ln.lower()
        if any(p in low for p in disallowed_patterns):
            iface_suspects.append(ln)

    gateways = []
    for m in re.finditer(r"(default\s+(?:via\s+)?)(\d{1,3}(?:\.\d{1,3}){3})", routes_blob, re.IGNORECASE):
        gateways.append(m.group(2))
    for m in re.finditer(r"^\s*0\.0\.0\.0\s+0\.0\.0\.0\s+(\d{1,3}(?:\.\d{1,3}){3})", routes_blob, re.MULTILINE):
        gateways.append(m.group(1))
    gateways = list(dict.fromkeys(gateways))

    dns_ips = extract_ipv4s(dns_blob)
    flagged_dns = [ip for ip in dns_ips if (ip not in allowed_dns)] if allowed_dns else []

    wifi_indicators = bool(wifi_blob.strip()) and not re.search(r"(no such|not found)", wifi_blob, re.IGNORECASE)
    bt_indicators = bool(bt_blob.strip()) and not re.search(r"(no such|not found)", bt_blob, re.IGNORECASE)

    fw_enabled = None
    if firewall_blob.strip():
        low = firewall_blob.lower()
        if re.search(r"\bstate\s+on\b", low) or "enabled" in low or "active" in low or "running" in low:
            fw_enabled = True
        if re.search(r"\bstate\s+off\b", low) or "disabled" in low or "inactive" in low:
            fw_enabled = False

    checks = []
    if allow_default_gw:
        checks.append({"check": "default_gateway_allowed", "pass": True, "details": "Policy allows a default gateway."})
    else:
        checks.append({"check": "no_default_gateway", "pass": (len(gateways) == 0), "details": {"detected_gateways": gateways}})
    checks.append({"check": "no_disallowed_interfaces", "pass": (len(iface_suspects) == 0), "details": {"matches": iface_suspects}})
    checks.append({"check": "dns_allowed", "pass": (len(flagged_dns) == 0), "details": {"flagged_dns": flagged_dns}})
    checks.append({"check": "wifi_not_present_or_disabled", "pass": (not wifi_indicators), "details": {"indicator": wifi_indicators}})
    checks.append({"check": "bluetooth_not_present_or_disabled", "pass": (not bt_indicators), "details": {"indicator": bt_indicators}})
    checks.append({"check": "firewall_enabled", "pass": True if fw_enabled is None else bool(fw_enabled), "details": {"status": "unknown" if fw_enabled is None else ("enabled" if fw_enabled else "disabled")}})

    overall_pass = all(bool(c.get("pass", False)) for c in checks)

    return {
        "policy_name": policy.get("policy_name", "unnamed"),
        "overall_pass": overall_pass,
        "checks": checks,
        "normalized": {
            "interfaces_suspect_lines": iface_suspects,
            "detected_gateways": gateways,
            "dns_extracted": dns_ips,
            "dns_flagged": flagged_dns,
            "wifi_indicator": wifi_indicators,
            "bluetooth_indicator": bt_indicators,
            "firewall_enabled": fw_enabled,
        },
    }


def tcp_connect_test(host: str, port: int, timeout_s: int) -> Dict[str, Any]:
    start = _dt.datetime.utcnow()
    ok = False
    err = None
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ok = True
    except Exception as e:
        err = str(e)
    end = _dt.datetime.utcnow()
    return {
        "host": host,
        "port": port,
        "ok": ok,
        "error": err,
        "duration_ms": int((end - start).total_seconds() * 1000),
        "time_utc": utcnow_iso(),
    }


def ping_once(ip: str, timeout_ms: int) -> bool:
    sysname = platform.system().lower()
    if "windows" in sysname:
        cmd = f"ping -n 1 -w {int(timeout_ms)} {ip}"
    elif "darwin" in sysname or "mac" in sysname:
        cmd = f"ping -c 1 -W 1 {shlex.quote(ip)}"
    else:
        sec = max(1, int((timeout_ms + 999) / 1000))
        cmd = f"ping -c 1 -W {sec} {shlex.quote(ip)}"
    return run_cmd(cmd, timeout=max(2, int((timeout_ms + 999) / 1000) + 2)).ok


def subnet_discovery(cidr: str, timeout_ms: int, concurrency: int) -> Dict[str, Any]:
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = [str(h) for h in net.hosts()]
    found: List[str] = []
    lock = threading.Lock()
    idx = {"i": 0}

    def worker():
        while True:
            with lock:
                if idx["i"] >= len(hosts):
                    return
                ip = hosts[idx["i"]]
                idx["i"] += 1
            if ping_once(ip, timeout_ms=timeout_ms):
                with lock:
                    found.append(ip)

    threads = []
    concurrency = max(1, min(int(concurrency), 256))
    for _ in range(concurrency):
        t = threading.Thread(target=worker, daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    found_sorted = sorted(found, key=lambda s: tuple(int(x) for x in s.split("."))) if found else []
    return {"cidr": str(net), "hosts_tested": len(hosts), "responsive_hosts": found_sorted}


def render_md(meta: Dict[str, Any], analysis_obj: Dict[str, Any], extra: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"# {TOOL_DISPLAY_NAME} Report")
    lines.append("")
    lines.append(f"- **Host**: `{meta.get('host')}`")
    lines.append(f"- **Platform**: `{meta.get('platform')}`")
    lines.append(f"- **Time (UTC)**: `{meta.get('time_utc')}`")
    lines.append(f"- **Policy**: `{analysis_obj.get('policy_name')}`")
    lines.append(f"- **Overall**: `{'PASS' if analysis_obj.get('overall_pass') else 'FAIL'}`")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for c in analysis_obj.get("checks", []):
        lines.append(f"- **{c.get('check')}**: `{'PASS' if c.get('pass') else 'FAIL'}`")
    lines.append("")
    if extra.get("connectivity_test"):
        lines.append("## Connectivity test (optional)")
        lines.append("")
        for item in extra["connectivity_test"]:
            label = item.get("label") or f"{item.get('host')}:{item.get('port')}"
            lines.append(f"- `{label}` → `{'REACHABLE' if item.get('ok') else 'not reachable'}` ({item.get('duration_ms')} ms)")
        lines.append("")
    if extra.get("subnet_scan"):
        s = extra["subnet_scan"]
        lines.append("## Subnet discovery (optional)")
        lines.append("")
        lines.append(f"- CIDR: `{s.get('cidr')}`")
        lines.append(f"- Hosts tested: `{s.get('hosts_tested')}`")
        lines.append(f"- Responsive hosts: `{len(s.get('responsive_hosts') or [])}`")
        lines.append("")
    lines.append("## Evidence")
    lines.append("")
    lines.append("Raw command outputs are under `raw/` and integrity hashes are in `hashes.txt`.")
    lines.append("")
    return "\n".join(lines)


def build_bundle(output_root: Path, host: str) -> Path:
    ts = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bundle = output_root / f"{host}_{ts}"
    safe_mkdir(bundle)
    safe_mkdir(bundle / "raw")
    return bundle


def write_hashes(bundle: Path) -> None:
    hashes_path = bundle / "hashes.txt"
    lines = []
    for p in sorted(bundle.rglob("*")):
        if p.is_file() and p.name != "hashes.txt":
            rel = p.relative_to(bundle).as_posix()
            lines.append(f"{sha256_file(p)}  {rel}")
    write_text(hashes_path, "\n".join(lines) + "\n")


def cmd_run(args: argparse.Namespace) -> int:
    policy = load_policy(Path(args.policy).resolve())
    output_root = Path(args.output).resolve()
    safe_mkdir(output_root)

    host = hostname()
    bundle = build_bundle(output_root, host)
    raw_dir = bundle / "raw"

    meta = {
        "host": host,
        "platform": platform.platform(),
        "time_utc": utcnow_iso(),
        "tool": {"name": TOOL_DISPLAY_NAME, "version": TOOL_VERSION},
    }

    evidence = collect_evidence(raw_dir=raw_dir)
    analysis_obj = analyze(policy=policy, evidence=evidence)
    extra: Dict[str, Any] = {}

    ct = policy.get("connectivity_test", {}) if isinstance(policy.get("connectivity_test"), dict) else {}
    if bool(ct.get("enabled", False)):
        timeout_s = int(ct.get("timeout_seconds", 2))
        results = []
        for t in ct.get("targets", []) or []:
            if not isinstance(t, dict):
                continue
            host_t = str(t.get("host", "")).strip()
            if not host_t:
                continue
            port_t = int(t.get("port", 443))
            label = str(t.get("label", "")).strip()
            r = tcp_connect_test(host_t, port_t, timeout_s)
            r["label"] = label
            results.append(r)
        extra["connectivity_test"] = results

        if any(r.get("ok") for r in results) and not policy.get("allow_default_gateway", False):
            analysis_obj.setdefault("checks", []).append({
                "check": "public_connectivity_not_reachable",
                "pass": False,
                "details": "One or more public targets were reachable via TCP connect.",
            })
            analysis_obj["overall_pass"] = False

    if args.scan_subnet:
        cidr = str(args.scan_subnet).strip()
        subnet_cfg = policy.get("subnet_scan", {}) if isinstance(policy.get("subnet_scan"), dict) else {}
        max_prefix = int(subnet_cfg.get("max_prefixlen", 24))
        net = ipaddress.ip_network(cidr, strict=False)
        if net.prefixlen < max_prefix and not bool(args.i_understand_large_scan):
            raise SystemExit(
                f"Refusing to scan {cidr} (prefixlen {net.prefixlen}) because it is larger than /{max_prefix}. "
                f"Re-run with --i-understand-large-scan if you truly intend this."
            )
        timeout_ms = int(subnet_cfg.get("ping_timeout_ms", 500))
        concurrency = int(subnet_cfg.get("concurrency", 64))
        extra["subnet_scan"] = subnet_discovery(cidr, timeout_ms=timeout_ms, concurrency=concurrency)

    report = {"meta": meta, "policy": policy, "analysis": analysis_obj, "evidence": evidence, "extra": extra}
    write_json(bundle / "report.json", report)
    write_text(bundle / "report.md", render_md(meta, analysis_obj, extra))
    write_hashes(bundle)

    print(str(bundle))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    bundle = Path(args.bundle).resolve()
    hashes_path = bundle / "hashes.txt"
    if not hashes_path.exists():
        raise SystemExit("hashes.txt not found in bundle")

    expected = {}
    for line in hashes_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            expected[parts[1]] = parts[0]

    missing, mismatches = [], []
    for rel, h in expected.items():
        p = bundle / rel
        if not p.exists():
            missing.append(rel)
            continue
        actual = sha256_file(p)
        if actual.lower() != h.lower():
            mismatches.append((rel, h, actual))

    if not missing and not mismatches:
        print("OK: bundle integrity verified")
        return 0

    if missing:
        print("MISSING FILES:")
        for rel in missing:
            print(f"  - {rel}")
    if mismatches:
        print("HASH MISMATCHES:")
        for rel, exp, act in mismatches:
            print(f"  - {rel}\n    expected: {exp}\n    actual:   {act}")
    return 2


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="gapcheck", description=f"{TOOL_DISPLAY_NAME} - air-gap compliance evidence collector.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="collect evidence and generate a report bundle")
    p_run.add_argument("--policy", required=True, help="path to policy JSON file")
    p_run.add_argument("--output", required=True, help="output directory root")
    p_run.add_argument("--scan-subnet", default=None, help="optional CIDR to ping-sweep (e.g., 192.168.10.0/24)")
    p_run.add_argument("--i-understand-large-scan", action="store_true", help="allow scans larger than policy max_prefixlen")
    p_run.set_defaults(func=cmd_run)

    p_ver = sub.add_parser("verify", help="verify hashes in an evidence bundle")
    p_ver.add_argument("--bundle", required=True, help="path to a bundle folder containing hashes.txt")
    p_ver.set_defaults(func=cmd_verify)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
