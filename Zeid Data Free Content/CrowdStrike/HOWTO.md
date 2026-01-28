# HOWTO — Implement Zeid Data AI Governance & Noise Reduction Pack in CrowdStrike Falcon
# comments: deposit ghost trace (copper)

This guide maps to the 4 deliverables shipped in this pack.

---

## Deliverable 1 — Host group segmentation + policy scoping

### Goal
Make tuning safe by ensuring changes are applied to **the smallest possible segment** of the fleet.

### Step-by-step
1) **Adopt the taxonomy**
- Start with `01-host-groups/host_group_taxonomy.md`
- Minimum recommended tiers:
  - `TIER-DC`
  - `TIER-SERVER-PROD`
  - `TIER-SERVER-NONPROD`
  - `TIER-WKS-PROD`
  - `TIER-WKS-DEV`
  - `TIER-BUILD`
  - `TIER-VIP`

2) **Implement tags**
Use stable tags you can set automatically:
- `zd_tier={dc|server|workstation|build|vip}`
- `zd_env={prod|stage|dev}`
- `zd_role={domain_controller|sql|app|citrix|...}`
- `zd_team={it|secops|data|...}`

See: `01-host-groups/tag_strategy.md`

3) **Create host groups in Falcon**
Create host groups based on those tags (avoid hostname regex unless you control naming strictly).

4) **Define policy scope**
Fill in:
- `01-host-groups/policy_scope_matrix.csv`

5) **Evidence to retain**
- Host groups list + membership rules
- Policy assignment matrix (by host group)
- Exceptions list + approvals

**Monthly hygiene**
- Drift check: assets missing `zd_tier` or `zd_env`
- Review membership rules for accuracy

---

## Deliverable 2 — Noise reduction with exclusions (guardrailed)

### Goal
Reduce false positives and repetitive alerts **without creating blind spots**.

### The decision tree
1) **Known-good binary with stable signer?**
- Prefer **certificate-based** approaches

2) **Known-good file/path, signer not stable**
- Use **ML exclusions** (tight scope, specific path, expiration)

3) **Benign behavior pattern**
- Use **IOA exclusions** (behavior-specific, scope to the smallest host group)

4) **Last resort**
- Avoid broad “visibility” style exclusions unless you have a documented reason and compensating controls

### Process
1) Pull last 14–30 days of detections (from your SIEM/LogScale or Falcon exports)
2) Identify the top recurring noise sources (top 10)
3) For each candidate exclusion:
   - business justification
   - ticket ID
   - approver name + date
   - expiration date (30–90 days)
   - scope host group(s)

Track everything in:
- `02-exclusions/exclusions_register.csv`
Policy guidance:
- `02-exclusions/exclusion_policy.md`

### Using the scripts
1) **Set env vars**
Copy:
- `02-exclusions/scripts/cs_env_example.env` → `.env`

2) **Install deps**
```bash
pip install -r 02-exclusions/scripts/requirements.txt
```

3) **Validate**
```bash
python 02-exclusions/scripts/validate_exclusions.py   --ml-csv 02-exclusions/sample_ml_exclusions.csv   --ioa-csv 02-exclusions/sample_ioa_exclusions.csv
```

4) **Export baseline**
```bash
python 02-exclusions/scripts/export_exclusions.py --out baseline_exports
```

5) **Create exclusions (start with dry-run)**
```bash
python 02-exclusions/scripts/create_ml_exclusions_from_csv.py   --csv 02-exclusions/sample_ml_exclusions.csv   --dry-run
```

Then (after approval/change window), run without `--dry-run`.

> Tip: Do not bulk-create exclusions until you’ve proven the scope is correct on a pilot host group.

### Review cadence
- Weekly: top noisy detection review
- Monthly: review expiring exclusions
- Quarterly: audit-style review of exclusions by category and scope

---

## Deliverable 3 — Falcon Fusion triage automation blueprints

### Goal
Standardize triage and reduce paging by ensuring humans only get high-signal alerts.

### Start with two workflows
Reference:
- `03-fusion/fusion_workflow_blueprints.md`
- `03-fusion/triage_routing_rules.yaml` (logic examples)

**Workflow A — Route by tier**
- Trigger: Detection created
- Conditions:
  - If `TIER-DC` / `TIER-SERVER-PROD` / `TIER-VIP` → escalate + notify + ticket
  - Else → standard queue, no ticket (unless high threshold)

**Workflow B — Ticket only above threshold**
- Trigger: Detection created
- Conditions:
  - severity >= High
  - confidence >= Medium
  - not on “expected admin activity” list
- Actions:
  - create ticket
  - add labels and enrichment notes

### Audit evidence for Fusion
- Export workflow definitions/screenshots (monthly or after changes)
- Keep change tickets that show who modified logic and why

---

## Deliverable 4 — Monthly evidence bundle

### Goal
Create a repeatable package you can hand to auditors.

### Run
```bash
pip install -r 04-evidence-bundle/scripts/requirements.txt

python 04-evidence-bundle/scripts/build_monthly_evidence_bundle.py   --days 30   --out evidence_out/2026-01
```

### Outputs
- `ml_exclusions.json`
- `cert_exclusions.json`
- `ioa_exclusions.json` (best effort; depends on module/scope)
- `rtr_audit_sessions.json` (best effort; depends on module/scope)
- `scheduled_reports.json` (best effort; depends on module/scope)
- `evidence_summary.json` (what succeeded/failed)
- `manifest_sha256.json` (integrity hashes)

### Storage + integrity
- Store bundle in restricted storage
- Make read-only after creation
- Keep the SHA256 manifest with the bundle

### Monthly checklist
Use:
- `04-evidence-bundle/templates/monthly_evidence_checklist.md`

---

## Operational guardrails (recommended)
- No global exclusions
- No exclusions without ticket + expiration
- Use pilot rings for policy changes
- Review scope drift monthly
- Keep evidence bundles immutable after creation
