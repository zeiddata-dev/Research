# Zeid Data Research — Taxonomy

This document defines what belongs where in this repo and how to label it. The goal is simple: anyone should be able to land here and immediately know where to find (or place) tools, write-ups, detections, dashboards, and public drops.

## Core categories

### Projects (`/projects`)
**Definition:** Runnable tools and utilities that produce outputs (reports, bundles, exports) or automate a workflow.

**Belongs here if it:**
- has a CLI/script/app someone can run,
- has configuration and repeatable output,
- is intended to be used as a tool (not just read).

**Common contents:**
- source code (`src/`)
- entry scripts (`scripts/`)
- examples (`examples/`)
- tests (`tests/`)
- packaged builds (`releases/`)

**Minimum requirements:**
- `README.md` with Quickstart
- `project.yaml` with status and entrypoints

**Example paths:**
- `projects/gapcheck/`
- `projects/genaiguard/`
- `projects/netledger/`

---

### Research (`/research`)
**Definition:** Analysis, notes, investigations, and supporting artifacts that are meant to be read, cited, or referenced.

**Belongs here if it:**
- explains a finding, issue, or technique,
- documents a CVE, incident pattern, malware family, or risk,
- includes references and mitigations,
- may include a PoC *only if it is safe and appropriate for defensive use*.

**Common contents:**
- write-up (`README.md`)
- indicators (`iocs/`)
- mitigations (`mitigations/`)
- references (`references.md`)
- safe sample data (`samples/` sanitized)

**Suggested sub-taxonomy:**
- `research/cve/<year-id>/`
- `research/malware/<family>/`
- `research/ops/<topic>/` (operational learnings)
- `research/threat-models/<domain>/`

**Example paths:**
- `research/cve/2025-20393/`
- `research/malware/qilin/`

---

### Detections (`/detections`)
**Definition:** Queries, rules, and hunting content meant to detect behaviors or indicators across vendors and telemetry sources.

**Belongs here if it:**
- is a SIEM query, EDR hunt, firewall rule, or correlation logic,
- is vendor-formatted content (Splunk, Sentinel, CrowdStrike, etc.),
- is a standardized rule format (Sigma, Suricata, YARA).

**Structure patterns:**
- Vendor packs: `detections/vendor-packs/<pack-name>/<vendor>/...`
- Standard formats: `detections/sigma/`, `detections/suricata/`, `detections/yara/`

**Minimum requirements for a vendor pack:**
- pack-level `README.md` (what it detects, how to deploy, tuning)
- one folder per vendor with deploy notes and artifacts

**Example paths:**
- `detections/vendor-packs/claude-bot/splunk/`
- `detections/vendor-packs/claude-bot/cisco/`

---

### Workbooks (`/workbooks`)
**Definition:** Dashboards and visualization artifacts that complement detections and investigations.

**Belongs here if it:**
- is a Sentinel workbook, Splunk dashboard, saved search bundle, etc.,
- provides panels and visual correlation views,
- is meant to be imported into a platform UI.

**Common contents:**
- dashboard/workbook JSON
- screenshots for preview
- `README.md` with install/import steps

**Example paths:**
- `workbooks/sentinel/`
- `workbooks/splunk/`

---

### Templates (`/templates`)
**Definition:** Reusable documentation and scaffolding for evidence, audit packaging, governance routines, and reporting.

**Belongs here if it:**
- is a form/checklist/policy scaffold,
- supports audit readiness (chain-of-custody, evidence bundle layout),
- helps teams standardize governance reporting.

**Common contents:**
- markdown templates (`.md`)
- doc templates (`.docx` optional)
- CSV schemas
- example filled-out sample (sanitized)

**Example paths:**
- `templates/audit-ready/`
- `templates/chain-of-custody/`
- `templates/ai-governance/`

---

### Drops (`/drops`)
**Definition:** Public, shareable releases (often tied to a post or announcement) that package content for quick adoption.

**Belongs here if it:**
- is designed to be shared externally as a “drop”,
- bundles multiple artifacts into a ready-to-consume package,
- needs a stable folder name tied to a date.

**Naming:**
- `drops/YYYY-MM-DD-short-title/`

**Common contents:**
- `README.md` with install/deploy steps
- `assets/` (images for social posts)
- `pack/` (the actual deliverables, zips, checksums)
- references back to canonical sources under `projects/` or `detections/`

**Example path:**
- `drops/2026-02-08-claude-detection/`

---

### Media (`/media`)
**Definition:** Images and public assets used across docs, drops, and readmes.

**Belongs here if it:**
- is a screenshot, diagram, or brand asset,
- is referenced by markdown in multiple places.

**Example paths:**
- `media/brand/`
- `media/screenshots/`
- `media/social/`

---

### Docs (`/docs`)
**Definition:** Repository-level documentation about how this repo works.

**Belongs here if it:**
- explains structure and standards,
- defines naming/versioning/evidence expectations,
- provides contributor guidance beyond root files.

**Example paths:**
- `docs/index.md`
- `docs/taxonomy.md`
- `docs/standards/naming.md`
- `docs/standards/evidence.md`

## Decision rules

Use these rules when deciding where something goes.

1. **If you can run it → `projects/`**  
   Even if it includes documentation, the primary identity is “tool.”

2. **If you can deploy it as a rule/query → `detections/`**  
   If it’s content consumed by a vendor platform, it’s detections.

3. **If you can import it as a dashboard → `workbooks/`**  
   Visualization artifacts live here, even if they complement detections.

4. **If it’s mainly read/cite → `research/`**  
   Write-ups, analysis, references, and supporting artifacts.

5. **If it’s a reusable form/checklist/scaffold → `templates/`**

6. **If it’s meant to be shared as a release → `drops/`**  
   Drops can reference (or include copies of) artifacts from other folders, but should not become the canonical home for long-term maintenance.

7. **If it’s an image or public asset → `media/`**

## Module maturity (status)

Every project and pack should include a `status` in `project.yaml`:

- `incubating` — prototype, moving fast
- `beta` — usable, still changing
- `stable` — ready for broad adoption
- `archived` — frozen for reference

## Required files by category

- **Project:** `README.md`, `project.yaml`
- **Research item:** `README.md`, `references.md` (recommended)
- **Vendor pack:** pack `README.md`, vendor subfolders with deploy notes
- **Workbook:** `README.md` describing import steps
- **Drop:** `README.md` with “what it is / how to use / what’s inside”

## Naming standards

- Use **kebab-case** for folder names: `attestation-ssh`, `stack-crasher`
- CVEs use `YYYY-NNNNN` format: `research/cve/2025-20393/`
- Drops use date prefix: `drops/2026-02-08-claude-detection/`

See: `docs/standards/naming.md`

## Notes on safety and responsibility

This repo is intended for defensive, audit-ready, evidence-first work. Research content should prioritize:
- mitigations and detection guidance,
- clear references,
- safe examples and sanitized samples,
- avoiding publication of harmful exploit-ready material.

When in doubt, keep the content defensive and focused on detection, hardening, and validation.
