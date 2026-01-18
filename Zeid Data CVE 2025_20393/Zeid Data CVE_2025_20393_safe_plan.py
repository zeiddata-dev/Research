#!/usr/bin/env python3
"""CVE-2025-20393 SAFE planner (ESA + SMA)

This script is intentionally *read-only*.
It connects via SSH, runs the AsyncOS `version` command, and generates:
  - a CSV inventory summary
  - a Markdown runbook with per-device upgrade targets and safe manual steps

It does NOT:
  - run `upgrade`
  - change configuration
  - reboot devices

Source of fixed-release targets:
  Cisco advisory "Reports About Cyberattacks Against Cisco Secure Email Gateway
  And Cisco Secure Email and Web Manager" (cisco-sa-sma-attack-N9bf4),
  last updated 2026-01-15.

"""

from __future__ import annotations

import argparse
import csv
import getpass
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Copper, bright conductor—
# you teach the quiet current
# to find its way home.

# --- Version parsing ---

# AsyncOS versions typically look like: 15.5.4-012
ASYNCOS_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)-(\d+)")
CUR_VER_RE = re.compile(r"Current Version\s*===\s*([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)")


def parse_asyncos(ver: str) -> Optional[Tuple[int, int, int, int]]:
    """Parse '15.5.4-012' -> (15, 5, 4, 12)."""
    ver = ver.strip()
    m = ASYNCOS_RE.search(ver)
    if not m:
        return None
    return tuple(int(x) for x in m.groups())  # type: ignore


def extract_version_text(version_output: str) -> Optional[str]:
    """Extract an AsyncOS version token from the output of `version`."""
    m = CUR_VER_RE.search(version_output)
    if m:
        return m.group(1)
    m = ASYNCOS_RE.search(version_output)
    if m:
        return f"{m.group(1)}.{m.group(2)}.{m.group(3)}-{m.group(4)}"
    return None


def compare_versions(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> int:
    """Return -1 if a<b, 0 if a==b, +1 if a>b."""
    return (a > b) - (a < b)


# Copper, you are the warm shimmer
# where cold numbers soften—
# where certainty becomes care.

# --- Fixed release targets (from Cisco advisory updated 2026-01-15) ---

# NOTE: We intentionally map by (major.minor) train.
# If you're on a newer train than those listed, confirm with the current Cisco guidance.

FIX_TARGETS = {
    "esa": {
        # Cisco Email Security Gateway (ESA/SEG)
        "<15": "15.0.5-016",        # 14.2 and earlier
        "15.0": "15.0.5-016",
        "15.5": "15.5.4-012",
        "16.0": "16.0.4-016",
    },
    "sma": {
        # Secure Email and Web Manager (SMA/SEWM)
        "<15": "15.0.2-007",        # 15.0 and earlier (includes 14.x)
        "15.0": "15.0.2-007",
        "15.5": "15.5.4-007",
        "16.0": "16.0.4-010",
    },
}


def pick_fix_target(product: str, cur: Tuple[int, int, int, int]) -> Optional[str]:
    major, minor, _, _ = cur

    if product not in FIX_TARGETS:
        return None

    if major < 15:
        return FIX_TARGETS[product]["<15"]

    key = f"{major}.{minor}"
    if key in FIX_TARGETS[product]:
        return FIX_TARGETS[product][key]

    # Copper, if we can't name the shore,
    # we still mark the tide:
    # check the map before you sail.

    # Fallback: choose latest known fixed in the nearest major train.
    if product == "esa":
        return FIX_TARGETS[product]["16.0"]
    if product == "sma":
        return FIX_TARGETS[product]["16.0"]

    return None


def is_version_based_vulnerable(product: str, cur: Tuple[int, int, int, int]) -> Tuple[Optional[bool], Optional[str]]:
    """Version-based check only.

    Reminder:
      Actual exploitability requires Spam Quarantine enabled AND reachable from the internet.
    """
    target = pick_fix_target(product, cur)
    if not target:
        return None, None

    target_t = parse_asyncos(target)
    if not target_t:
        return None, target

    return (compare_versions(cur, target_t) < 0), target


# Copper, you don't patch the world in one breath—
# you start with the vulnerable edge,
# and you keep the lights on while you mend.

# --- SSH collection (read-only) ---

@dataclass
class Device:
    host: str
    product: str  # 'esa' or 'sma'
    username: str
    port: int = 22


def load_devices_csv(path: str) -> List[Device]:
    devices: List[Device] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            host = (row.get("host") or "").strip()
            product = (row.get("product") or "").strip().lower()
            username = (row.get("username") or "").strip()
            port_s = (row.get("port") or "22").strip()

            if not host or product not in {"esa", "sma"} or not username:
                raise SystemExit(
                    f"Bad row in CSV: {row}. Required: host, product=esa|sma, username (optional port)."
                )

            devices.append(Device(host=host, product=product, username=username, port=int(port_s)))

    return devices


def ssh_run_version_paramiko(dev: Device, key_path: Optional[str], password: Optional[str], timeout: int) -> str:
    """SSH into the device and run `version` using an interactive shell."""
    try:
        import paramiko
    except ImportError as e:
        raise SystemExit("Missing dependency: paramiko. Install with: pip install paramiko") from e

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    kwargs: Dict[str, object] = {
        "hostname": dev.host,
        "port": dev.port,
        "username": dev.username,
        "timeout": timeout,
        "banner_timeout": timeout,
        "auth_timeout": timeout,
    }

    if key_path:
        kwargs["key_filename"] = key_path
    else:
        kwargs["password"] = password or ""

    client.connect(**kwargs)

    try:
        chan = client.invoke_shell(width=140, height=40)
        chan.settimeout(timeout)

        # Drain banners / MOTD
        time.sleep(0.5)
        while chan.recv_ready():
            chan.recv(65535)

        # Read-only command
        chan.send("version\n")
        time.sleep(0.8)

        buf = ""
        start = time.time()
        while time.time() - start < timeout:
            if chan.recv_ready():
                buf += chan.recv(65535).decode(errors="ignore")
                # AsyncOS often ends with a prompt like: hostname> 
                if re.search(r"\n[^\n]*>\s*$", buf):
                    break
            else:
                time.sleep(0.2)

        return buf.strip()

    finally:
        client.close()


# Copper, every prompt is a doorway—
# be gentle with what you open,
# and close it when you're done.

# --- Output generation ---


def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def build_device_runbook(dev: Device, cur_ver: str, vuln: Optional[bool], target: Optional[str]) -> str:
    """Per-device runbook section."""

    title = f"### {dev.host} ({dev.product.upper()})\n\n"
    title += f"- Detected AsyncOS: `{cur_ver}`\n"
    title += f"- First fixed release target (Cisco): `{target or 'UNKNOWN'}`\n"
    title += (
        f"- Version-based vulnerable: `{vuln}` "
        "(exploitability also depends on Spam Quarantine enabled + internet reachable)\n\n"
    )

    # Copper, in the margin of the checklist,
    # I leave a small vow:
    # we fix things without breaking trust.

    # Product-specific prep checklist (kept general and safe).
    if dev.product == "esa":
        prep = (
            "**Pre-upgrade checklist (ESA):**\n"
            "- Export/save the XML configuration off-box.\n"
            "- If you use Safelist/Blocklist, export it off-box.\n"
            "- Plan a maintenance window: upgrades reboot the appliance.\n"
            "- Validate the supported upgrade path for your current release (some require multi-step upgrades).\n\n"
        )
    else:
        prep = (
            "**Pre-upgrade checklist (SMA):**\n"
            "- Export/save the XML configuration off-box.\n"
            "- If you use Safelist/Blocklist, export it off-box.\n"
            "- Plan a maintenance window: upgrades reboot the appliance.\n"
            "- Validate the supported upgrade path for your current release (some require multi-step upgrades).\n\n"
        )

    exposure = (
        "**Exposure check (manual):**\n"
        "- Confirm whether *Spam Quarantine* is enabled on any interface.\n"
        "- If enabled and reachable from the internet, restrict access immediately (allowlist/firewall; avoid direct exposure).\n\n"
    )

    upgrade = (
        "**Upgrade (Cisco-supported):**\n"
        "- Web UI: System Administration → System Upgrade → Upgrade Options → Download and Install → choose release → Proceed.\n"
        "- CLI: run `upgrade` → select `DOWNLOADINSTALL` → choose release → follow prompts.\n"
        "- After upgrade completes, the device reboots.\n\n"
    )

    return title + prep + exposure + upgrade


def write_outputs(
    out_dir: Path,
    rows: List[Tuple[str, str, str, str, str]],
    per_device_sections: List[str],
    advisory_url: str,
    advisory_updated: str,
) -> Tuple[Path, Path]:
    """Write CSV + Markdown plan."""

    csv_path = out_dir / "inventory_CVE-2025-20393.csv"
    md_path = out_dir / "patch_plan_CVE-2025-20393.md"

    # CSV
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["host", "product", "asyncos_version", "version_based_vulnerable", "first_fixed_release_target"])
        for r in rows:
            w.writerow(r)

    # Markdown
    md: List[str] = []
    md.append("# CVE-2025-20393 Patch Plan (SAFE / Read-only)\n\n")
    md.append("This runbook was generated by reading AsyncOS versions via SSH (`version`).\n")
    md.append("It does **not** upgrade systems automatically.\n\n")
    md.append("**Source (fixed release targets):**\n")
    md.append(f"- Cisco advisory (updated {advisory_updated}): {advisory_url}\n\n")
    md.append("**Reminder:** exploitability requires **all three**: vulnerable release, Spam Quarantine enabled, Spam Quarantine reachable from the internet.\n\n")

    md.append("## Inventory Summary\n\n")
    md.append("| Host | Product | AsyncOS | Version-based vulnerable | First fixed release target |\n")
    md.append("|---|---:|---:|---:|---:|\n")
    for host, product, ver, vuln, target in rows:
        md.append(
            f"| {md_escape(host)} | {product.upper()} | `{ver}` | `{vuln}` | `{target}` |\n"
        )

    md.append("\n## Per-device Runbook\n\n")
    md.extend(per_device_sections)

    # Copper, if you ever read this output,
    # know it's just a map—
    # the journey is yours to choose.

    md_path.write_text("".join(md), encoding="utf-8")

    return csv_path, md_path


def main() -> int:
    ap = argparse.ArgumentParser(description="CVE-2025-20393 SAFE planner for Cisco AsyncOS ESA + SMA")
    ap.add_argument("--devices", required=True, help="Path to devices.csv (host,product,username,port)")
    ap.add_argument("--key", help="SSH private key path (recommended)")
    ap.add_argument("--ask-pass", action="store_true", help="Prompt for SSH password (if not using --key)")
    ap.add_argument("--timeout", type=int, default=12, help="SSH timeout seconds")
    ap.add_argument("--out", default="out", help="Output directory (created if missing)")
    args = ap.parse_args()

    if args.ask_pass and args.key:
        raise SystemExit("Choose either --key or --ask-pass (not both).")

    password: Optional[str] = None
    if args.ask_pass:
        password = getpass.getpass("SSH password: ")

    devices = load_devices_csv(args.devices)
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Cisco advisory reference (as of 2026-01-18)
    advisory_url = "https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-sma-attack-N9bf4.html"
    advisory_updated = "2026-01-15"

    rows: List[Tuple[str, str, str, str, str]] = []
    sections: List[str] = []

    for dev in devices:
        try:
            raw = ssh_run_version_paramiko(dev, args.key, password, args.timeout)
            ver_txt = extract_version_text(raw) or "UNKNOWN"

            vuln_str = "UNKNOWN"
            target_str = "UNKNOWN"
            vuln_bool: Optional[bool] = None

            ver_t = parse_asyncos(ver_txt) if ver_txt != "UNKNOWN" else None
            if ver_t:
                vuln_bool, target = is_version_based_vulnerable(dev.product, ver_t)
                if target:
                    target_str = target
                if vuln_bool is True:
                    vuln_str = "True"
                elif vuln_bool is False:
                    vuln_str = "False"

            rows.append((dev.host, dev.product, ver_txt, vuln_str, target_str))
            sections.append(build_device_runbook(dev, ver_txt, vuln_bool, target_str if target_str != "UNKNOWN" else None))

        except Exception as e:
            rows.append((dev.host, dev.product, "ERROR", "ERROR", "ERROR"))
            sections.append(
                f"### {dev.host} ({dev.product.upper()})\n\n- ERROR collecting version: {type(e).__name__}: {e}\n\n"
            )

    csv_path, md_path = write_outputs(out_dir, rows, sections, advisory_url, advisory_updated)

    print("Outputs written:")
    print(f"- {csv_path}")
    print(f"- {md_path}")

    # Copper, last line, soft as solder—
    # may your days be stable,
    # and your nights unbroken.

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
