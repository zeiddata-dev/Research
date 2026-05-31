<!-- ZEID DATA README HERO START -->
![Zeid Data scripts banner](../../assets/banners/readme/scripts.png)

<p align="center">
  <a href="../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="."><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![automation](https://img.shields.io/badge/automation-2EA043?style=flat-square) ![scripts](https://img.shields.io/badge/scripts-334155?style=flat-square) ![cli-tools](https://img.shields.io/badge/cli%20tools-334155?style=flat-square) ![tooling](https://img.shields.io/badge/tooling-334155?style=flat-square) ![validators](https://img.shields.io/badge/validators-334155?style=flat-square) ![tools](https://img.shields.io/badge/tools-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data Research Scripts

This folder contains evidence-first defensive tooling for detection engineering, hunting, auditing, validation, collection, and repeatable maintenance tasks.

Scripts here should be boring in the useful way: clear inputs, predictable outputs, explicit limits, and no surprise damage.

## What this is for

Use `tools/scripts/` for small runnable helpers that support:

- Detection engineering.
- Threat hunting.
- Validation and control testing.
- Evidence generation and packaging.
- Repo maintenance and documentation automation.
- Local transforms or inventory generation.

If a tool grows into a standalone product with its own config, tests, docs, and release flow, move it to [`projects/`](../../projects).

## Supported script types

This repo may include multiple ecosystems:

- PowerShell: Windows process, persistence, scheduled task, and audit checks.
- KQL: Microsoft Sentinel and Defender hunts.
- SPL: Splunk searches and correlation logic.
- Sigma: portable detection rules.
- YARA: defensive scanning rules.
- Zeek: network behavior detections.
- Python: automation, transforms, validators, and evidence generation.
- Bash: lightweight Linux checks and repo maintenance.

## Naming conventions

Use clear names with the `zeid_data_` prefix when practical.

Examples:

- `zeid_data_hunt_ransomware_fileshare.py`
- `zeid_data_sentinel_ransomware_prep.kql`
- `zeid_data_sigma_ransomware_prep.yml`
- `zeid_data_zeek_firstseen_largepost.zeek`
- `zeid_data_Hunt-NewScheduledTasks.ps1`

## Recommended layout

```text
tools/scripts/
  docs/
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
```

Create folders when real content exists. Empty structure is not documentation. It is furniture with no building.

## Script header expectations

Every script should include or link to:

- Purpose.
- Intended telemetry source or input files.
- Required permissions.
- Dependencies.
- Safe usage example.
- Expected output.
- Failure modes.
- Tuning notes and allowlists, if applicable.

## Evidence-first output expectations

Scripts should prefer outputs that are easy to store and defend.

Recommended fields:

- Timestamp in UTC when practical.
- Host or device identifier.
- User or account, if relevant and public-safe.
- Source file, table, index, or telemetry source.
- Match reason, rule name, threshold, or keyword hit.
- Output path.
- Warnings and skipped items.

Preferred output formats:

- JSONL.
- JSON.
- CSV.
- Markdown summaries generated from structured output.

## Safety and scope

This repo is for defensive security and auditing.

Do not add:

- Exploit code.
- Credential theft tooling.
- Misuse instructions.
- Stealth or evasion tooling for unauthorized activity.
- Private logs, tokens, or sensitive customer data.

Simulation content must use synthetic inputs and safe training patterns.

## Contributing checklist

When adding a script:

- [ ] Name is clear.
- [ ] Purpose is documented.
- [ ] Inputs are documented.
- [ ] Outputs are documented.
- [ ] Required permissions are documented.
- [ ] Example run is included.
- [ ] Failure modes or limitations are listed.
- [ ] Examples are sanitized.

## Related docs

- [`docs/automation.md`](../../docs/automation.md)
- [`docs/taxonomy.md`](../../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../../docs/standards/evidence.md)

## License

Unless otherwise noted in a specific file, scripts in this directory follow the repository license.
