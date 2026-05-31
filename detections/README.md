<!-- ZEID DATA README HERO START -->
![Zeid Data detections banner](../assets/banners/readme/detections.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../tools/scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data Detections

This folder is for defensive detection engineering: Sigma rules, SIEM queries, vendor packs, hunting logic, and analytics that can be deployed or adapted in controlled environments.

The standard is evidence over vibes. A useful detection explains what it looks for, what data it needs, how to validate it, and where false positives are likely to come from.

## What belongs here

- Sigma, YARA, Suricata, KQL, SPL, EDR queries, and NDR logic.
- Vendor-specific packs for platforms such as Microsoft Sentinel, Splunk, CrowdStrike, SentinelOne, Cisco, Zeek, firewall tools, or similar systems.
- Detection write-ups that include data source requirements and validation steps.
- Safe simulation notes that use synthetic or public-safe samples.

## What does not belong here

- Exploit instructions.
- Credential theft tooling.
- Stealth, evasion, persistence, or bypass guidance intended for unauthorized use.
- Private logs, customer telemetry, secrets, tokens, or sensitive infrastructure details.

## Minimum detection documentation

Each detection or pack should include:

| Field | Requirement |
|---|---|
| Purpose | What behavior, condition, or signal the detection is intended to identify. |
| Data sources | Required telemetry, tables, indexes, event IDs, fields, or log types. |
| Logic | Query, rule, thresholds, joins, filters, and assumptions. |
| Tuning | Known benign patterns, allowlist guidance, expected noise sources. |
| Validation | Safe test method, sample event, replay method, or expected match condition. |
| Output | Alert fields, evidence fields, dashboard panel, or report schema. |
| Limits | What the detection does not prove and what data gaps break it. |

## Recommended layout

```text
detections/
  sigma/
  yara/
  suricata/
  sentinel/
  splunk/
  zeek/
  vendor-packs/
    pack-name/
      README.md
      sentinel/
      splunk/
      sigma/
```

Use the smallest structure that matches the artifact. Do not create empty hierarchy just to look enterprise.

## Review checklist

Before publishing a detection:

- [ ] It is defensive and authorized.
- [ ] Required telemetry is listed.
- [ ] Query or rule logic is readable.
- [ ] False positives are documented.
- [ ] Validation path is included.
- [ ] Output fields are listed.
- [ ] Examples are sanitized.
- [ ] Claims are tied to evidence or marked as unvalidated.

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`docs/automation.md`](../docs/automation.md)
