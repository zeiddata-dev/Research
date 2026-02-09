# Zeid Data Research Labs — Scripts

This directory contains practical security and audit-oriented scripts used for detection engineering, threat hunting, validation, and evidence generation across common enterprise telemetry sources.

The goal is simple:

If it didn’t generate evidence, it didn’t happen.

---

## What you’ll find here

Scripts are organized by purpose and telemetry source. Expect a mix of:

- Endpoint hunts (Windows/Linux process, persistence, staging, ransomware prep)
- Network analytics (Zeek, DNS/TLS, HTTP behavior, first-seen + burst detection)
- SIEM queries (Microsoft Sentinel KQL, Splunk SPL)
- Rules-as-code (Sigma, YARA)
- Auditing helpers (inventory, policy validation, retention checks, evidence packaging)

This folder may include both:
- Drop-in scripts (single-file, runnable)
- Detection snippets (queries/rules meant to be copied into your platform)

---

## Naming conventions

All scripts should follow:

- Prefix: zeid_data_
- Descriptive file name
- Use an extension that matches the ecosystem

Examples:
- zeid_data_hunt_ransomware_fileshare.py
- zeid_data_sentinel_ransomware_prep.kql
- zeid_data_sigma_ransomware_prep.yml
- zeid_data_zeek_firstseen_largepost.zeek
- zeid_data_Hunt-NewScheduledTasks.ps1

---

## Directory layout (recommended)

As this directory grows, keep scripts easy to browse:

scripts/
  endpoint/
    windows/
    linux/
  network/
    zeek/
    dns/
    tls/
  siem/
    sentinel/
    splunk/
  rules/
    sigma/
    yara/
  auditing/
    evidence/
    retention/
    inventory/
  docs/

If you’re adding a new script and it fits a category above, place it there.

---

## Supported script types

PowerShell (.ps1)
Typical use: Windows process creation, persistence, scheduled task hunting.
Common dependencies:
- Sysmon (recommended)
- Windows Security auditing (4688 command line enabled)
- Admin or appropriate log read permissions

Microsoft Sentinel KQL (.kql)
Typical use: hunting and analytics in Microsoft Defender and Log Analytics.
Common tables used:
- DeviceProcessEvents
- DeviceNetworkEvents
- SecurityEvent

Splunk SPL (.spl)
Typical use: process telemetry hunts, exfil tooling detection, correlation searches.
Assumes normalized fields where possible, but scripts may include coalesce() to reduce friction.

Sigma (.yml)
Detection portability format intended for conversion into platform-native rules.

YARA (.yar)
Heuristic or signature-style scanning helpers. Many rules are intentionally conservative and should be tuned to reduce false positives.

Zeek (.zeek)
Network behavior detections using Zeek logs and analyzers (HTTP, DNS, TLS).

Python (.py)
Automation, file share sweeps, evidence generation, local data transforms.

Bash (.sh)
Linux checks and lightweight audit and persistence sweeps.

---

## How to use

1) Read the header first
Most scripts include:
- Intended telemetry source
- Required permissions
- Expected output
- Tuning tips and allowlists

2) Run in a test environment
- Validate against known benign baselines
- Add allowlists for admin tools and maintenance windows
- Confirm output format matches your evidence workflows

3) Promote into your platform
- Convert Sigma to SIEM rules
- Turn KQL/SPL into scheduled analytics rules
- Track versions and changes in Git

---

## Evidence-first output expectations

Scripts should prefer outputs that are easy to store and defend.

Recommended fields:
- Timestamp (UTC preferred)
- Host or device identifier
- User or account
- Process image and full command line
- Parent process (when available)
- Network destination (domain/IP/port) when relevant
- Match reason (keyword hit, rule name, threshold)

When practical, produce output in:
- JSONL
- CSV
- or a clean console table that can be exported

---

## Safety and scope

This repo is intended for defensive security and auditing.

- No exploit code
- No credential theft tooling
- No instructions for misuse
- Any simulation content must use synthetic inputs and safe training patterns

If a contribution could be dual-use, it will be rejected or rewritten into a safe training version.

---

## Contributing

When adding a new script, include:
- A short header block with purpose, prerequisites, usage, and tuning notes
- Clear assumptions (what logs/tables are required)
- Output schema notes (what fields it emits)
- A brief example run or example output

---

## License

Unless otherwise noted in a specific file, scripts in this directory follow the repository license.

---

## Disclaimer

Zeid Data Research Labs scripts are provided as-is for educational and operational support. You are responsible for validating fit, accuracy, and compliance requirements in your environment.
