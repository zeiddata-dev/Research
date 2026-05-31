# Zeid Data Research Taxonomy

This document defines what belongs where in the public research repo. The goal is simple: a visitor should be able to tell whether something is a tool, detection, research note, workbook, template, or public content without reverse-engineering the folder tree.

## Core categories

| Area | Path | Use it for |
|---|---|---|
| Content | `content/` | Vendor-organized guidance, field notes, public-safe packs, and reusable evidence material. |
| Detections | `detections/` | Rules, queries, logic, and analytics intended for SIEM, EDR, NDR, firewall, or other security platforms. |
| Docs | `docs/` | Repo standards, maintenance guidance, taxonomy, automation plans, and operating rules. |
| Projects | `projects/` | Runnable tools, prototypes, apps, utilities, and repeatable workflows. |
| Research | `research/` | Write-ups, investigations, malware notes, CVE notes, threat models, and white papers. |
| Tools and scripts | `tools/scripts/` | Small automation helpers, validators, collectors, and evidence generators. |
| Templates | `templates/` | Reusable reporting, evidence, incident, audit, and governance templates. |
| Workbooks | `workbooks/` | Dashboards, saved searches, workbook JSON, visual analytics, and importable views. |
| Assets | `assets/` | Banners, images, screenshots, diagrams, and public-safe visual material. |

## Decision rules

Use these rules when adding new material.

1. If someone runs it, put it under `projects/` or `tools/scripts/`.
2. If a platform imports it as a rule, query, or analytic, put it under `detections/`.
3. If a platform imports it as a dashboard or saved visualization, put it under `workbooks/`.
4. If it is mainly analysis to read and cite, put it under `research/`.
5. If it is reusable documentation scaffolding, put it under `templates/`.
6. If it explains repo policy or structure, put it under `docs/`.
7. If it is a screenshot, banner, or diagram, put it under `assets/`.

## Required files by category

| Category | Required documentation | Recommended metadata |
|---|---|---|
| Project | `README.md` with purpose, quickstart, outputs, safety notes | `project.yaml` with status, owner, tags, entrypoints |
| Detection pack | Pack `README.md` with data sources, logic, tuning, deployment notes | `status`, platform, telemetry, false-positive notes |
| Research item | `README.md` or named Markdown write-up with references | `last_reviewed`, status, public-safe flag, references |
| Script folder | `README.md` with naming, usage, output schema expectations | supported runtimes and validation commands |
| Workbook | `README.md` with import steps, data sources, screenshots if possible | platform, required tables, known limitations |
| Template | Header explaining when to use it and what to fill in | version, owner, last reviewed |

## Status model

Use one of these statuses when adding metadata:

- `draft`: early or incomplete. Needs review before use.
- `incubating`: usable experiment, still changing.
- `beta`: usable with documented limits.
- `stable`: reviewed and ready for broader reuse.
- `archived`: preserved for reference, not actively maintained.

## Evidence model

Any artifact that claims to detect, validate, audit, or summarize should identify its evidence path.

Minimum evidence fields:

- input source or telemetry source
- assumptions
- command, query, or logic used
- output location or output schema
- validation steps
- known limitations

No unsupported scoring. No fake completeness claims. If the repo does not contain enough evidence, mark the gap.

## Public-safe rule

This repo is public. Do not commit secrets, private logs, customer identifiers, access tokens, sensitive infrastructure details, or exploit-ready abuse instructions.

Defensive research can still be practical. Keep the useful parts: detections, mitigations, validation, safe test data, and references.
