# Zeid Data Research — Docs Index

This repo is organized like a lab: tools you can run, detections you can deploy, research you can cite, and drops you can share.

## Quick navigation

- **Run a tool:** `../projects/`
- **Read write-ups / analysis:** `../research/`
- **Deploy detections:** `../detections/`
- **Import dashboards / workbooks:** `../workbooks/`
- **Use templates (evidence, audit, governance):** `../templates/`
- **Find images and assets:** `../media/`
## Repo map

- `../projects/`  
  Shipped tools and runnable code. Each project should have a clear Quickstart and predictable layout.

- `../research/`  
  Write-ups, analyses, and supporting artifacts (IOCs, mitigations, references). CVEs and malware research live here.

- `../detections/`  
  Detection content organized by vendor pack and/or standardized formats (Sigma, Suricata, YARA).

- `../workbooks/`  
  Dashboards, workbooks, saved searches, and visualizations.

- `../templates/`  
  Audit-ready templates: evidence bundles, chain-of-custody docs, governance checklists, reporting scaffolds.


- `../media/`  
  Public media (brand assets, screenshots, diagrams) used across docs and drops.

- `../docs/`  
  Repository standards and documentation (this folder).

## How to choose the right path

Use this guide when adding or searching for something:

- If it’s **runnable** (CLI, script, app) → `../projects/<name>/`
- If it’s **analysis** (CVE note, incident write-up, threat research) → `../research/...`
- If it’s **rules/queries** for vendors/SIEMs → `../detections/...`
- If it’s **dashboards** → `../workbooks/...`
- If it’s **a shareable release** for social/email → `../drops/YYYY-MM-DD-title/`
- If it’s **reusable documentation** (evidence forms, checklists) → `../templates/...`

## Standard module layout

Every module (project, pack, or research folder) should follow a predictable structure.

Recommended baseline:

<module>/
README.md
project.yaml
docs/
scripts/
src/
examples/
tests/
releases/


Use what you need; keep it consistent.

## Naming and organization standards

- **Folder names:** kebab-case (`attestation-ssh`, `stack-crasher`, `claude-bot`)
- **Drops:** date-prefixed (`YYYY-MM-DD-short-title`)
- **Vendor packs:** one folder per vendor inside the pack
- **One purpose per folder:** avoid dumping unrelated items into a module root

See: `./standards/naming.md`

## Evidence-first expectations

If a tool or pack claims it supports audit readiness, it should produce (or help produce) outputs that are:

- deterministic (same input → same output),
- timestamped,
- traceable (inputs, config, and environment noted),
- exportable (JSON/CSV/MD/PDF where appropriate),
- easy to bundle (zip-ready structure).

See: `./standards/evidence.md`

## Releases

Use `releases/` for packaged artifacts:

- versioned zip(s)
- `SHA256SUMS` (or similar)
- brief release notes (or reference to root `CHANGELOG.md`)

Suggested naming:

- `<name>-vX.Y.Z.zip`
- `SHA256SUMS.txt`

## Status model

Add a `status` field to `project.yaml`:

- `incubating` — ideas / early prototypes
- `beta` — usable, still changing
- `stable` — ready for broad use
- `archived` — kept for reference

## project.yaml example

Use lightweight metadata to keep the repo easy to scan:

```yaml
name: gapcheck
version: 0.2.0
status: beta
owner: zeiddata
tags: [compliance, evidence, auditing]
last_reviewed: 2026-02-08
entrypoints:
  - scripts/gapcheck.py
outputs:
  - reports/*.json
  - reports/*.csv
