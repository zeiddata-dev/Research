<!-- ZEID DATA README HERO START -->
![Zeid Data templates banner](../assets/banners/readme/templates.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../tools/scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![templates](https://img.shields.io/badge/templates-334155?style=flat-square) ![reporting](https://img.shields.io/badge/reporting-334155?style=flat-square) ![documentation](https://img.shields.io/badge/documentation-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data Security Templates

This folder contains ready-to-copy templates for repeatable security, audit, research, reporting, and operational work.

Templates should reduce ambiguity. A good template tells the next person what to collect, what to prove, what to fill in, what to leave blank when evidence is missing, and what should never be guessed.

## What belongs here

Common template types:

- Detection templates: behavior, data sources, logic, tuning, validation.
- Incident response templates: triage steps, containment, timeline, evidence checklist.
- Threat hunting templates: hypothesis, query set, expected signals, decision path.
- Risk and compliance templates: control objective, evidence, reviewer notes, gaps.
- Change management templates: change description, impact, rollback, approvals.
- Runbooks and playbooks: step-by-step operating procedures.
- Research note templates: scope, sources, analysis, defensive value, limits.

## How to use these templates

1. Copy the closest template to your use case.
2. Fill in environment-specific fields such as vendor, log source, owner, severity, and scope.
3. Test in a non-production or limited-scope context when commands or detections are involved.
4. Document outcomes, false positives, gaps, tuning decisions, and evidence references.
5. Promote only after review and tracking.

## Minimum fields to complete

Most templates should require:

- Owner or responsible team.
- Purpose.
- Scope.
- Data sources.
- Procedure, detection logic, query, or workflow.
- Evidence to collect.
- Expected output.
- Known gaps or missing evidence.
- References.
- Last reviewed date.

## Template quality rules

- Keep instructions short and executable.
- Use checkboxes for repeatable review steps.
- Prefer tables for evidence fields and decision records.
- Never force a fake value. Use `evidence missing`, `not evaluated`, or `not applicable` when appropriate.
- Include safe placeholders instead of private examples.
- Track versions when a template may be reused externally.

## Suggested metadata block

```yaml
---
title: Example Template
status: draft
owner: zeid-data
last_reviewed: 2026-05-31
category: template
tags: [evidence, security, reporting]
public_safe: true
---
```

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`docs/automation.md`](../docs/automation.md)

## Disclaimer

These templates are starting points. Validate them against your policies, legal requirements, privacy requirements, and production environment before use.
