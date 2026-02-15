# Zeid Data Research

Zeid Data Research is a technical repository of defensive security engineering artifacts: reproducible investigations, CVE and malware analysis, detection engineering packs, and audit-grade evidence scaffolding.

This repo is designed for operators who need determinism, traceability, and deployable outputs across SIEM, EDR, network, and cloud telemetry.

## Repository layout

- `projects/`  
  Runnable tools and utilities (CLI/scripts/apps). If you can run it, it belongs here.

- `research/`  
  Technical write-ups and investigations: CVEs, malware families, telemetry studies, incident patterns, and threat models.

- `detections/`  
  Detection logic by vendor pack and/or standardized formats (Sigma, Suricata, YARA). Includes tuning guidance and telemetry prerequisites.

- `workbooks/`  
  Dashboards and workbooks (Sentinel, Splunk, etc.) intended for import into platform UIs.

- `templates/`  
  Audit-ready scaffolding: evidence bundles, chain-of-custody, governance checklists, reporting structures.

- `media/`  
  Public diagrams, screenshots, and share assets referenced by docs and drops.

- `docs/`  
  Repo standards and navigation:
  - `docs/index.md` (how to navigate)
  - `docs/taxonomy.md` (what goes where)
  - `docs/standards/naming.md` (naming rules)
  - `docs/standards/evidence.md` (evidence expectations)

## What “Research” means here

A research module is the canonical source of truth for:
- threat model and assumptions
- reproducible methodology
- artifacts (IOCs, queries, rules, samples where appropriate)
- mitigations and validation steps
- references and provenance

If something is primarily runnable as a tool, it belongs in `projects/` and research should link to it.

## Research module structure (technical standard)

Research lives under:
- `research/cve/YYYY-NNNNN/`
- `research/malware/<family>/`
- `research/ops/<topic>/`
- `research/threat-models/<domain>/`

Minimum viable research module:
- `README.md` (primary write-up)
- `references.md` (primary sources)
- `iocs/` (indicators with provenance)
- `mitigations/` (hardening + verification)

Recommended additions:
- `detections/` (derived rules/queries)
- `pcaps/` (sanitized)
- `samples/` (sanitized)
- `repro/` (reproduction harness, defensive-oriented)
- `figures/` (diagrams, timelines)
- `field-mapping.md` (telemetry mapping per platform)
- `assumptions.md` (explicit constraints)

## Evidence-first expectations

If a module claims “audit-ready,” it should produce outputs that are:
- deterministic (same input + config => same output)
- traceable (what ran, when, with what settings)
- exportable (JSON/CSV/MD/PDF as needed)
- readable (human review without guesswork)

Recommended run output structure:
- `reports/run-metadata.json`
- `reports/findings.json`
- `reports/findings.csv`
- `reports/summary.md`

For packaged artifacts in `releases/`, include:
- versioned zip(s)
- `SHA256SUMS.txt`

## Detection engineering principles

Detections are behavior-first:
- prefer sequences and correlations over atomic indicators
- bind to stable invariants (protocol semantics, auth workflow constraints)
- document telemetry dependencies (required fields and fidelity)
- include tuning guidance and known false-positive discriminators

If a detection correlates sources, document:
- join keys and cardinality
- time window and skew tolerance
- failure modes (missing lineage, NAT flattening, clock drift)

## IOC standards (required for research modules)

Store indicators under `iocs/` with provenance and time bounds.

Recommended files:
- `iocs/domains.csv`
- `iocs/ips.csv`
- `iocs/hashes.csv`
- `iocs/urls.csv`

Recommended required columns:
- `indicator`
- `type` (domain|ip|sha256|url|registry|email|user-agent|cert)
- `first_seen`
- `last_seen`
- `source`
- `confidence` (low|medium|high)
- `context`
- `tags`

Never commit secrets or customer-identifying data. Sanitize aggressively and document redaction in `summary.md`.

## Telemetry normalization guidance

Prefer normalized keys when writing detections and describing observables:

- time: `event_time` (ISO 8601 with timezone)
- principal: `user`, `user_id`, `device_id`, `host`
- process: `process_name`, `process_path`, `process_sha256`, `parent_process_*`
- network: `src_ip`, `dst_ip`, `dst_port`, `protocol`, `dns_qname`, `tls_sni`, `http_host`, `ja3`, `ja4`, `cert_sha256`
- cloud: `account_id`, `tenant_id`, `app_id`, `resource`, `api_operation`

When platform fields differ, include `field-mapping.md`:
- platform field name
- normalized alias
- type, nullability, examples
- join suitability (high/medium/low)

## Safety and responsible publication

This repository is defensive and operational. Research should prioritize:
- mitigations and detection guidance
- safe, sanitized examples
- reproduction that supports defense and validation

Avoid publishing exploit-ready automation or weaponized content. When in doubt, keep content detection- and hardening-focused.

## Contributing

Submit work that is:
- reproducible
- evidence-backed (artifacts, methodology, or primary sources)
- properly placed per taxonomy
- named per standards

Before opening a PR, check:
- `docs/taxonomy.md`
- `docs/standards/naming.md`
- `docs/standards/evidence.md`

## License and security

- See `LICENSE.md` for licensing.
- See `SECURITY.md` for vulnerability reporting and sensitive disclosures.
