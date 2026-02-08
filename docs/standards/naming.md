# Naming Standards

These conventions keep the repo predictable, searchable, and easy to maintain as it grows.

## Goals

- predictable paths and filenames
- low ambiguity (clear what something is and where it belongs)
- stable URLs (links don’t break when content expands)
- easy grepping and automation

## Folder naming

### General rule
Use **kebab-case** for all folders.

✅ Good
- `projects/genaiguard/`
- `projects/attestation-ssh/`
- `detections/vendor-packs/claude-bot/`
- `research/malware/qilin/`

❌ Avoid
- `Zeid Data GenAIGuard/`
- `Claude Bot Detection Pack/`
- `CVE_2025_20393/`
- `GenAIGuard_v2/`

### Where to use abbreviations
Prefer **full words** unless the abbreviation is universally recognized in security/compliance.

✅ Acceptable
- `cve`
- `ioc` / `iocs`
- `siem`
- `edr`
- `tls`
- `dns`
- `yara`
- `sigma`

❌ Avoid
- `misc`
- `stuff`
- `temp`
- `newnew`
- `final`

## Module naming

A **module** is anything you can point to as a unit:
- a project tool under `projects/`
- a detection pack under `detections/vendor-packs/`
- a research item under `research/`

### Project module names
Use a short, clear name that matches how you speak about it.

✅ Good
- `gapcheck`
- `netledger`
- `genaiguard`
- `stack-crasher`

If you need to differentiate, add a clarifier:
- `gapcheck-agent`
- `gapcheck-reporter`
- `genaiguard-extension`

### Detection pack names
Use a short behavior or subject name.
- `claude-bot`
- `ai-egress`
- `credential-dumping`
- `ransomware-staging`

Avoid vendor names as pack names unless the pack is vendor-specific by design.

## CVE naming

CVE folders must be:

research/cve/YYYY-NNNNN/


Example:
- `research/cve/2025-20393/`

Do not use underscores or “CVE_” prefixes in folder names.

## Malware naming

Malware research folders must be:

drops/YYYY-MM-DD-short-title/


✅ Good
- `drops/2026-02-08-claude-detection/`
- `drops/2026-03-01-ai-egress-baseline/`

Rules:
- date is the release/publication date
- title is 2–5 words max
- no versions in folder name (versions live in artifacts)

## Vendor folders

Inside `detections/vendor-packs/<pack>/`, vendors use kebab-case and should be recognizable.

✅ Good
- `splunk/`
- `sentinel/`
- `crowdstrike/`
- `cisco/`
- `snowflake/`
- `databricks/`

If you support multiple products per vendor, nest one more level:
- `cisco/asa/`
- `cisco/ftd/`

## Filenames

### General
- use **kebab-case** for filenames
- prefer `.md` for docs, `.yml/.yaml` for config, `.json` for exports

✅ Good
- `howto.md`
- `false-positives.md`
- `field-mapping.md`
- `sigma-rules.yml`
- `workbook.json`

❌ Avoid
- `HOWTO_FINAL2.md`
- `myNotes(1).md`
- `dashboard new.json`

### Standard filenames (recommended)

Repo root:
- `README.md`
- `LICENSE.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

Module root:
- `README.md`
- `project.yaml`
- `howto.md` (optional)
- `references.md` (research)
- `field-mapping.md` (detections)

## Version naming

### Where versions go
- `project.yaml` contains the authoritative version.
- packaged artifacts go in `releases/`.

### Artifact naming

Use:<module>-vX.Y.Z.<ext>


Examples:
- `gapcheck-v0.2.0.zip`
- `claude-bot-v0.1.0.zip`

Include checksums:
- `SHA256SUMS.txt`

Do not put versions in folder names.

## Dates and timestamps

### Dates in paths
Use ISO format:
- `YYYY-MM-DD`

### Dates in reports/logs
Use ISO 8601 timestamps when possible:
- `2026-02-08T14:32:10Z`
- `2026-02-08T08:32:10-06:00`

Avoid locale formats like `02/08/26`.

## IDs and slugs

When you need a short ID for an item (issue, pack, report, dataset):
- use lowercase alphanumeric + hyphen
- keep it short and stable

Example:
- `ai-egress-baseline`
- `tls-sni-anomaly`

## “One purpose per folder” rule

A folder name should tell you what’s inside. If you start mixing unrelated content:
- split it into subfolders, or
- create a new module.

✅ Good
- `detections/vendor-packs/claude-bot/splunk/`
- `workbooks/sentinel/`

❌ Avoid
- `projects/gapcheck/random-notes/`
- `research/malware/qilin/old-stuff/`

## Renaming policy

When renaming paths that might be referenced externally:
- preserve old links if possible (GitHub redirects help, but don’t rely on them)
- update references in:
  - `README.md`
  - `docs/index.md`
  - drop READMEs
- add a brief note to `CHANGELOG.md`

## Quick checklist

Before you commit:
- [ ] folders are kebab-case
- [ ] CVE folders use `YYYY-NNNNN`
- [ ] drops use `YYYY-MM-DD-…`
- [ ] filenames are kebab-case
- [ ] versions appear only in `project.yaml` and `releases/`
- [ ] no “final”, “misc”, “temp” in names

