# CVE-2025-20393 SAFE Planner (Cisco ESA + SMA)

A small **read-only** helper that:

- SSHes to Cisco AsyncOS appliances (**ESA/SEG** and **SMA/SEWM**)
- Runs the AsyncOS `version` command
- Compares your version to Cisco’s published **first fixed release** targets
- Generates:
  - `inventory_CVE-2025-20393.csv`
  - `patch_plan_CVE-2025-20393.md`

This is designed for **safe assessment + planning**, not for pushing upgrades automatically.

## Why “SAFE”?

The script **does not**:

- run `upgrade`
- modify config
- reboot appliances

It only reads version info, then writes local output files.

## Source of fixed-release targets

Targets are pulled from Cisco’s advisory:

- Cisco advisory: `cisco-sa-sma-attack-N9bf4`
- Updated: **2026-01-15**
- URL: https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-sma-attack-N9bf4.html

> Always verify targets against the latest Cisco guidance before upgrading.

## Requirements

- Python 3.9+ (3.10/3.11 preferred)
- Network reachability to appliance SSH
- Credentials with permission to run `version`
- Python dependency:
  - `paramiko`

Install dependency:

```bash
pip install paramiko
```

## Quick Start

1) Create `devices.csv`

```csv
host,product,username,port
esa-01.example.com,esa,admin,22
sma-01.example.com,sma,admin,22
```

2) Run the planner

Key-based auth (recommended):

```bash
python3 cve_2025_20393_safe_plan.py --devices devices.csv --key ~/.ssh/id_ed25519 --out out
```

Password-based auth:

```bash
python3 cve_2025_20393_safe_plan.py --devices devices.csv --ask-pass --out out
```

3) Review outputs

- `out/inventory_CVE-2025-20393.csv`
- `out/patch_plan_CVE-2025-20393.md`

## What the tool tells you (and what it does not)

- **It tells you**: whether your AsyncOS version is below the **first fixed release** for its train.
- **It does not tell you**: whether you are *actually exploitable*.

Exploitability depends on additional conditions (e.g., whether **Spam Quarantine** is enabled and reachable from the internet). Use the runbook to perform the manual exposure checks.

## Safety note

Upgrades reboot appliances. Use a maintenance window, validate upgrade paths, and follow your internal change control.

## License

Use at your own risk. No warranty.
