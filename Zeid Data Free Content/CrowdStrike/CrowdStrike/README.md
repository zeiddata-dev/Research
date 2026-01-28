# Zeid Data — CrowdStrike Content Pack

**Purpose:** Practical, operator-focused CrowdStrike Falcon content (queries, workflows, detections, and reporting) designed to reduce noise and increase auditability.

**Tagline:** _If it didn’t generate evidence, it didn’t happen._

---

## What this is

This repository contains **CrowdStrike Falcon** content curated and maintained by **Zeid Data** to help security teams:

- Improve signal quality and reduce alert fatigue
- Standardize investigations with repeatable workflows
- Produce defensible evidence for audits and incident reviews
- Accelerate detection engineering and tuning

---

## What’s included

Depending on the pack/release, you may find:

- **Queries & hunting** (Falcon Query Language / event search)
- **Detection logic** (behavior patterns, high-signal filters, tuning guidance)
- **Response workflows** (triage checklists, escalation paths, containment guidance)
- **Dashboards & reporting** (operational views, executive summaries, evidence exports)
- **Reference mappings** (MITRE ATT&CK notes, control objectives, common risk scenarios)

> Folder names and file types may vary by pack.

---

## Pack-level documentation (important)

Each individual content pack includes:

- Its own **README.md** describing scope, prerequisites, and deployment notes
- A **HOWTO.md** (or similarly named guide) with step-by-step usage instructions, validation steps, and tuning guidance

Start there first before importing or applying anything broadly.

---

## Intended audience

- SOC analysts and incident responders  
- Detection engineers / threat hunters  
- Security platform owners (Falcon admins)  
- GRC / audit partners who need **repeatable evidence**

---

## Quick start

1. **Pick a pack**
   - Navigate into the specific pack folder you want to use.

2. **Read the pack docs**
   - Review the pack’s **README.md** and **HOWTO.md** for prerequisites, assumptions, and safe rollout guidance.

3. **Import or copy the content**
   - Paste queries into Falcon search/hunt tooling.
   - Apply detection/tuning guidance gradually (start in “observe” mode when possible).

4. **Validate in your environment**
   - Run the included validation steps (if provided).
   - Confirm that results match your host groups, naming conventions, and expected baselines.

5. **Operationalize**
   - Add to your team runbooks.
   - Schedule recurring reviews for high-risk detections and drift checks.

---

## Safety and operational guidance

- **Test first:** Apply detection or policy changes in a limited scope before broad rollout.
- **Avoid breaking ops:** Some hardening actions can disrupt business workflows; coordinate with stakeholders.
- **Treat outputs as prompts, not truth:** Telemetry can be incomplete; corroborate with endpoint context and identity signals.

---

## Evidence philosophy

Zeid Data content is built around one simple idea:

> **If it didn’t generate evidence, it didn’t happen.**

Where possible, packs emphasize:
- Clear inputs (telemetry sources and assumptions)
- Reproducible queries
- Artifact capture (timestamps, host/user identifiers, query outputs)
- Consistent naming for audit trails

---

## Compatibility

- Designed for **CrowdStrike Falcon** environments.
- Some content may require specific Falcon modules/features (varies by pack).
- Your results will vary based on retention windows, sensor coverage, and policy configuration.

---

## Contributing

We welcome contributions that improve fidelity and operational usefulness:

- Fixes for false positives / false negatives
- Additional high-signal queries and tuning notes
- Better documentation, examples, and test cases

**How to contribute**
1. Fork the repo
2. Create a feature branch
3. Add/modify content with clear notes and example outputs (sanitized)
4. Open a pull request describing the problem and the change

---

## Support

If you want help deploying, tuning, or mapping this pack to your environment’s control objectives:

- Open an issue with a sanitized description (no sensitive artifacts)
- Or engage Zeid Data for implementation support

---

## Legal and disclaimer

- This repository is provided **as-is**, without warranty of any kind.
- Content is intended for defensive security purposes only.
- You are responsible for validating compliance, safety, and suitability in your environment.
- CrowdStrike and Falcon are trademarks of CrowdStrike, Inc. This project is **not affiliated with or endorsed by CrowdStrike**.

---

## Contact

**Zeid Data**  
Security engineering, governance, and evidence-driven operations.

security@zeiddata.com
