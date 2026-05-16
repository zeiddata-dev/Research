<!-- ZEID DATA README HERO START -->
![Zeid Data scripts banner](../../assets/banners/readme/scripts.png)

<p align="center">
  <a href="../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

```md
# Zeid Data Research Labs — Scripts 🧪🛠️
*Evidence-first defensive tooling for detection engineering, hunting, auditing, and “prove it” moments.*

If it didn’t generate evidence, it didn’t happen. ☠️  
If it *did* happen and you didn’t log it… congrats, you own a ghost story.

---

## What this is
This directory contains practical security and audit-oriented scripts used for:

- Detection engineering
- Threat hunting
- Validation and control testing
- Evidence generation and packaging

Across common enterprise telemetry sources (endpoint, network, SIEM, cloud, and whatever else is screaming today).

---

## What you’ll find here
Scripts are organized by purpose and telemetry source. Expect a mix of:

- **Endpoint hunts** (Windows/Linux process, persistence, staging, ransomware prep) 💻
- **Network analytics** (Zeek, DNS/TLS, HTTP behavior, first-seen + burst detection) 🌐
- **SIEM queries** (Microsoft Sentinel KQL, Splunk SPL) 📊
- **Rules-as-code** (Sigma, YARA) 🧩
- **Auditing helpers** (inventory, policy validation, retention checks, evidence packaging) 🧾

This folder may include both:
- **Drop-in scripts** (single file, runnable)
- **Detection snippets** (queries/rules meant to be copied into your platform)

The goal is boring on purpose: predictable inputs, defensible outputs, less “we think maybe…” during incidents.

---

## Naming conventions (chaos is expensive)
All scripts should follow:

- Prefix: `zeid_data_`
- Descriptive file name
- Extension that matches the ecosystem

Examples:
- `zeid_data_hunt_ransomware_fileshare.py`
- `zeid_data_sentinel_ransomware_prep.kql`
- `zeid_data_sigma_ransomware_prep.yml`
- `zeid_data_zeek_firstseen_largepost.zeek`
- `zeid_data_Hunt-NewScheduledTasks.ps1`

---

## Directory layout (recommended)
As this directory grows, keep it easy to browse:

tools/scripts/
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

If your script fits a category above, put it there. If it doesn’t… it probably needs its own folder (or a better name).

---

## Supported script types
This repo intentionally spans multiple ecosystems:

- **PowerShell (.ps1)**  
  Windows process creation, persistence, scheduled task hunting.  
  Common dependencies: Sysmon (recommended), Security auditing (4688 with command line), appropriate log permissions.

- **Microsoft Sentinel KQL (.kql)**  
  Hunting and analytics in Defender / Log Analytics.  
  Common tables: `DeviceProcessEvents`, `DeviceNetworkEvents`, `SecurityEvent`.

- **Splunk SPL (.spl)**  
  Process telemetry hunts, exfil tooling detection, correlation searches.  
  Assumes normalized fields where possible; may use `coalesce()` to reduce friction.

- **Sigma (.yml)**  
  Portable detection format intended for conversion into platform-native rules.

- **YARA (.yar)**  
  Heuristic/signature scanning helpers. Many rules are conservative and should be tuned to reduce false positives.

- **Zeek (.zeek)**  
  Network behavior detections using Zeek logs/analyzers (HTTP, DNS, TLS).

- **Python (.py)**  
  Automation, file share sweeps, evidence generation, local transforms.

- **Bash (.sh)**  
  Lightweight Linux checks and persistence sweeps.

---

## How to use (please don’t YOLO this into prod)
1. **Read the header first**  
   Most scripts include:
   - Intended telemetry source
   - Required permissions
   - Expected output
   - Tuning tips and allowlists

2. **Run in a test environment**
   - Validate against known benign baselines
   - Add allowlists for admin tools and maintenance windows
   - Confirm output format matches your evidence workflows

3. **Promote into your platform**
   - Convert Sigma to SIEM-native rules
   - Turn KQL/SPL into scheduled analytics
   - Track versions and changes in Git

---

## Evidence-first output expectations 📂
Scripts should prefer outputs that are easy to store and defend.

Recommended fields:
- Timestamp (UTC preferred)
- Host/device identifier
- User/account
- Process image + full command line
- Parent process (when available)
- Network destination (domain/IP/port) when relevant
- Match reason (rule name, threshold, keyword hit, etc.)

Preferred output formats:
- JSONL
- CSV
- clean console tables (exportable)

The point is receipts. Not vibes.

---

## Safety and scope 🛡️
This repo is for defensive security and auditing.

- No exploit code
- No credential theft tooling
- No misuse instructions
- Any simulation content must use synthetic inputs and safe training patterns

If a contribution is dual-use, it will be rejected or rewritten into a safe training version.

---

## Contributing
When adding a new script, include:
- Short header block (purpose, prerequisites, usage, tuning notes)
- Clear assumptions (what logs/tables are required)
- Output schema notes (fields it emits)
- A brief example run or sample output

Make it usable for the next person who stumbles into this folder at 2:13 AM. 😬

---

## License
Unless otherwise noted in a specific file, scripts in this directory follow the repository license.

---

## Disclaimer
Zeid Data Research Labs scripts are provided as-is for educational and operational support.  
You are responsible for validating fit, accuracy, and compliance requirements in your environment.
```
