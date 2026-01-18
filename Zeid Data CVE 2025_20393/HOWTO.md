# Zeid Data - Copper Hang Back...
# HOWTO — CVE-2025-20393 SAFE Assessment + Patch Planning

This guide assumes you want **low-risk** steps:

- identify which appliances are below the first fixed release
- confirm whether you’re actually exposed
- perform upgrades **manually** using Cisco-supported flows

## 1) Build your device list

Create `devices.csv` in the same folder as the script:

```csv
host,product,username,port
esa-01.example.com,esa,admin,22
sma-01.example.com,sma,admin,22
```

Rules:
- `product` must be `esa` or `sma`
- `port` defaults to 22 if you omit it

## 2) Run the SAFE planner

Install dependency:

```bash
pip install paramiko
```

Run (key auth):

```bash
python3 cve_2025_20393_safe_plan.py --devices devices.csv --key ~/.ssh/id_ed25519 --out out
```

Run (password auth):

```bash
python3 cve_2025_20393_safe_plan.py --devices devices.csv --ask-pass --out out
```

## 3) Interpret the results

Open:

- `out/inventory_CVE-2025-20393.csv`
- `out/patch_plan_CVE-2025-20393.md`

If `version_based_vulnerable` is `True`, you should plan an upgrade to the `first_fixed_release_target`.

If it is `False`, you are **at or above** the first fixed release for that train.

If it is `UNKNOWN`, the script couldn’t parse the version output.

## 4) Confirm whether you’re *actually exposed* (manual)

Even if an appliance is on a vulnerable release, exploitability depends on configuration.

Recommended manual checks:

- Confirm whether **Spam Quarantine** is enabled on any interface.
- Confirm whether that interface is reachable from the internet.
- If enabled and reachable, restrict access immediately (allowlist/firewall, avoid direct exposure).

## 5) Prepare for an upgrade (manual)

Before upgrading:

- Export/save the appliance XML configuration off-box.
- Plan a maintenance window (upgrades reboot).
- Confirm the supported upgrade path for your current version (some trains require multi-step upgrades).

## 6) Upgrade using Cisco-supported methods

Use one of these:

### Web UI (typical)

- System Administration → System Upgrade
- Upgrade Options
- Download and Install
- Choose the target release
- Proceed

### CLI (interactive)

- run: `upgrade`
- select: `DOWNLOADINSTALL`
- choose the target release
- follow prompts

## 7) Verify after upgrade

- Re-run the SAFE planner and confirm `version_based_vulnerable=False`.
- Confirm management exposure is restricted.
- Confirm monitoring/log forwarding is in place.

## Reference

Cisco advisory (fixed release table + upgrade steps):

https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-sma-attack-N9bf4.html
