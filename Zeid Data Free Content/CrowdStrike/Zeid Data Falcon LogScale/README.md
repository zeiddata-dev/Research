# Zeid Data — CrowdStrike Falcon Audit Evidence + Noise Reduction Pack
# comments: deposit ghost trace (copper)

**Tagline:** *If it didn’t generate evidence, it didn’t happen.*

This is a practical customization pack for **CrowdStrike Falcon** focused on two outcomes:

- **Noise reduction** (fewer false positives, cleaner queues)
- **Audit evidence** (repeatable exports + integrity manifests you can hand to auditors)

It’s built as templates + scripts + runbooks you can adapt to your tenant and your change-control process.

---

## What this pack includes (the “4 deliverables”)

### 1) Host group segmentation + policy scoping
A starter taxonomy, tag strategy, and a **policy scope matrix** so tuning is safe and targeted (no “global” changes by accident).

### 2) Top-noise cleanup via guardrailed exclusions
Templates and scripts to manage exclusions with:
- narrow scoping (host groups)
- expiration dates
- justification + ticket references
- review cadence

### 3) Fusion triage automation blueprints
Blueprints for Falcon Fusion workflows to:
- route detections by asset tier (DC/server/VIP/workstation)
- enrich + label consistently
- create tickets only when thresholds are met

### 4) Monthly evidence bundle
A runbook + scripts that generate a **monthly evidence folder** containing:
- exclusion inventories
- RTR audit exports (where available)
- scheduled reports inventory (where available)
- an integrity manifest (SHA256)

---

## Who this is for
- SecOps / SOC engineers
- Detection engineering teams
- GRC / audit teams that need reproducible artifacts
- Platform owners who need to reduce alert fatigue without creating blind spots

---

## Requirements
- Python 3.10+
- CrowdStrike API client credentials with appropriate read (and optionally write) permissions
- A controlled workstation (do not run from random laptops)
- Change-control process for exclusions and policy changes

> This pack does not “turn on” features for you. You must implement the host groups, policies, and Fusion workflows in your Falcon tenant.

---

## Quick start

### 1) Configure credentials
Copy the env file and set credentials:
- `02-exclusions/scripts/cs_env_example.env` → `.env`

Required:
- `FALCON_CLIENT_ID`
- `FALCON_CLIENT_SECRET`

Optional:
- `FALCON_CLOUD` (example: `us-1`)

### 2) Install dependencies
```bash
pip install -r 02-exclusions/scripts/requirements.txt
pip install -r 04-evidence-bundle/scripts/requirements.txt
```

### 3) Validate your exclusion CSVs
```bash
python 02-exclusions/scripts/validate_exclusions.py   --ml-csv 02-exclusions/sample_ml_exclusions.csv   --ioa-csv 02-exclusions/sample_ioa_exclusions.csv
```

### 4) Export current exclusions (baseline)
```bash
python 02-exclusions/scripts/export_exclusions.py --out baseline_exports
```

### 5) Generate a monthly evidence bundle
```bash
python 04-evidence-bundle/scripts/build_monthly_evidence_bundle.py   --days 30   --out evidence_out/2026-01
```

---

## Folder structure
- `01-host-groups/` — taxonomy, tagging strategy, scope matrix
- `02-exclusions/` — exclusion policy, registers, sample CSVs, scripts
- `03-fusion/` — workflow blueprints + routing logic examples
- `04-evidence-bundle/` — runbook + evidence scripts + checklist templates
- `99-ops/` — security notes, changelog

---

## Security and audit posture
- Treat exclusions like controlled change:
  - ticket + approval + expiration + review notes
- Store evidence bundles in restricted storage and make them read-only after creation
- Use least-privilege API scopes; do not reuse personal tokens or admin “god” keys

---

## Important notes / limitations
- Falcon tenants vary by enabled modules and API scope availability.
- Some endpoints/operation IDs may differ across environments/SDK versions.
- The evidence scripts are designed to **degrade gracefully** and record what could not be exported.

---

## Trademark notice
CrowdStrike and Falcon are trademarks of CrowdStrike, Inc. This project is not affiliated with, endorsed by, or sponsored by CrowdStrike.

---

## License
Zeid Data — see `LICENSE.txt`
