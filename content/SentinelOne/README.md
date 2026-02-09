# Zeid Data — SentinelOne Content

Defensive, evidence-first content for operating and validating detections in SentinelOne Singularity environments.

This folder is built for practitioners who need repeatable detection engineering workflows, audit-friendly investigation notes, and practical playbooks that map telemetry to triage, containment, and recovery.

Guiding principle: If it didn’t generate evidence, it didn’t happen.

---

## What’s in this section

You will typically find content like:

1) Detections / Analytics
- Detection logic and operator guidance
- Tuning notes and common false positives
- Safe validation steps (no malware required)
- ATT&CK mapping and confidence notes
- Evidence requirements (what to export and preserve)

2) Hunting
- Hunt ideas that translate to SentinelOne investigations
- Queries, filters, and pivot strategies
- “What to look for next” decision trees

3) Threat Notes
- Tradecraft summaries aligned to observable behaviors
- Indicator handling guidance (scope, expiry, and context)
- Links to public references where applicable

4) Playbooks
- Triage checklists (first 5 minutes, first hour, first day)
- Containment and response actions with impact notes
- Remediation and recovery steps
- Post-incident evidence bundle templates

5) Reporting / Evidence Packs (optional)
- Audit-ready report templates
- Suggested KPIs (MTTD, MTTR, prevalence, top detections)
- Export guidance for defensible documentation

---

## Recommended folder structure

sentinelone/
  README.md
  detections/
    <detection_name>/
      README.md
      detection.md
      validation.md
      tuning.md
      attck_mapping.yaml
      evidence/
        fields.md
        sample_artifacts/
  hunting/
    README.md
    hunts/
      <hunt_name>.md
    pivot_guides/
      process_tree.md
      network_pivots.md
      persistence_pivots.md
  playbooks/
    <scenario_name>/
      README.md
      triage.md
      containment.md
      eradication.md
      recovery.md
      evidence_bundle.md
  reports/
    templates/
      incident_summary.md
      evidence_index.md
      executive_one_pager.md

Use this as a guideline. Keep it simple and consistent.

---

## Naming conventions

Use stable, searchable names:
- sentinelone-endpoint-<behavior>-<platform>
- Example: sentinelone-endpoint-suspicious-powershell-windows

Avoid putting dates in folder names unless necessary. Put version/date inside documents instead.

---

## Quick start workflow

Step 1: Pick your starting point
- If you are building or refining logic, start in detections/
- If you are responding to an alert pattern, start in playbooks/
- If you are exploring unknown activity, start in hunting/

Step 2: Confirm assumptions
Every item should clearly state:
- Required OS coverage (Windows/macOS/Linux)
- Required visibility/telemetry and feature dependencies
- Known gaps and “will not detect” conditions

Step 3: Validate safely
Use validation.md to confirm the behavior is observable without introducing malware. Validation should be reproducible in a lab and minimally disruptive.

Step 4: Tune with evidence
Tuning is not “make it quiet.” Tuning is “reduce noise without reducing security.”
All exclusions should include:
- justification
- scope (narrowest possible)
- owner
- review/expiration date
- evidence that the change reduces false positives without masking true positives

Step 5: Preserve evidence
If you can’t prove it later, it didn’t happen. Capture the minimum viable evidence bundle before making disruptive response changes.

---

## Evidence-first standards (required)

Every detection/playbook should answer these questions:

- What does this detect or address?
- Why does it matter (risk/impact)?
- What telemetry is required?
- How do I validate it safely?
- How do I triage it (what to check first)?
- What are common false positives and how do we tune them?
- What evidence must be preserved and how should it be exported?

Minimum evidence bundle guidance (adapt to your environment):
- Host identity: hostname, asset ID, IPs, OS, agent version
- Time window: first seen, last seen, timezone, event sequence notes
- Process context: process tree, parent/child, full command lines, user context
- File context: paths, hashes, signer info (if available), creation/modification times
- Network context: destination domains/IPs, ports, protocols, JA3/TLS notes if available
- Persistence context: services, autoruns, scheduled tasks, launch agents, registry keys
- Analyst notes: decision log, why actions were taken, what was ruled out

---

## SentinelOne environment notes

SentinelOne deployments vary by:
- agent versions and OS mix
- policy settings (prevention and response actions)
- retention, export access, and visibility
- feature availability by license tier

For every artifact, document:
- minimum requirements and assumptions
- what data fields are expected
- any limitations observed during testing

---

## Safety and scope

This repository content is defensive:
- No instructions intended to enable harm, compromise systems, or evade security controls
- Validation guidance must be non-destructive and appropriate for lab testing
- Any content discussing attacker techniques must be framed as detection, response, and safe simulation only

---

## Contribution guidelines

PRs welcome. When adding a new detection or playbook, include at minimum:
- README.md overview (purpose, scope, assumptions, required telemetry)
- detection.md or triage.md (operator steps)
- validation.md (safe validation steps)
- tuning.md (false positives, exclusions, and strategy)
- attck_mapping.yaml (technique mapping and confidence)
- evidence/fields.md (what evidence to export)

Quality checklist:
- Clear goal and scope
- Repeatable steps
- Safe validation
- Explicit assumptions
- Practical tuning guidance
- Evidence bundle requirements
- Change notes or versioning inside the doc

---

## Licensing and attribution

Unless otherwise noted, content follows the repository license.
If using external research, cite sources and summarize in your own words. Avoid copying large verbatim sections.

---

Zeid Data
