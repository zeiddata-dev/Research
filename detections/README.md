# Detections

This folder contains Zeid Data detection engineering content: vendor-specific hunting packs, platform-ready rules/queries, and standardized detection formats. The intent is to provide deployable detections that are evidence-first, operationally realistic, and easy to tune.

## What belongs here

Place content here if it is designed to detect behaviors or indicators using telemetry from:
- SIEMs (Splunk, Sentinel, etc.)
- EDR/XDR (CrowdStrike, etc.)
- Network controls (firewalls, DNS, proxy, NDR)
- Cloud and data platforms (Snowflake, Databricks, etc.)

If something is primarily a runnable tool, it belongs in `projects/`. If it is a technical write-up, it belongs in `research/`. Detections can and should link to both.

## Folder structure

Detections are organized in two primary ways:

1) Vendor packs (recommended for real deployments)
- `detections/vendor-packs/<pack-name>/<vendor>/...`

2) Standardized formats (optional but useful for portability)
- `detections/sigma/`
- `detections/suricata/`
- `detections/yara/`

Suggested structure:

detections/
  README.md
  vendor-packs/
    <pack-name>/
      README.md
      <vendor>/
        README.md
        queries/
        rules/
        dashboards/ (optional)
        samples/ (sanitized, optional)
  sigma/
  suricata/
  yara/

## Vendor pack standards

A vendor pack is a self-contained set of detections for a single subject area (behavior, tool, threat, or control objective).

Examples:
- `claude-bot`
- `ai-egress`
- `credential-dumping`
- `ransomware-staging`

Pack-level required file:
- `detections/vendor-packs/<pack-name>/README.md`

Vendor-level required file:
- `detections/vendor-packs/<pack-name>/<vendor>/README.md`

Each vendor README must clearly state:
- telemetry prerequisites (required data sources and fields)
- deployment steps
- tuning guidance (common false positives and suppressions)
- expected outputs (alerts, saved searches, dashboards)
- validation steps (how to confirm the detection works)

## Detection design requirements (technical)

Zeid Data detections are behavior-first and evidence-oriented.

### Required for every detection
Each rule/query must declare:

- Objective: what behavior is being detected and why it matters
- Telemetry dependencies:
  - required log source(s)
  - required fields
  - minimum fidelity (e.g., process lineage, TLS SNI, DNS logs)
- Logic: the detection itself with comments explaining invariants
- Tuning guidance:
  - expected false positives
  - discriminators to reduce noise
- Validation:
  - a simple test case or procedure to prove it fires correctly
  - how to confirm it is not overly broad

### Correlation guidance (when joining sources)
If the detection correlates multiple events (endpoint + network, DNS + TLS, auth + API):
- specify join keys (host + pid, user + session, src_ip + dst_ip)
- specify time window and skew tolerance (e.g., +/- 2 minutes)
- document cardinality assumptions (1:1, 1:N)
- document failure modes (NAT flattening, missing lineage, clock drift)

### Prefer stable invariants
Prefer invariants that survive minor attacker changes:
- protocol semantics (handshake behavior, auth workflow constraints)
- sequence and timing (ordered steps across telemetry)
- rare combinations (process + destination + user context)
- environment context (asset criticality, allowlists)

Avoid relying solely on:
- single domains
- single hashes
- static fingerprints without additional context (JA3/JA4 alone)

## Normalized field guidance

Where possible, express logic in normalized terms and map platform fields explicitly.

Recommended normalized keys:
- time: `event_time` (ISO 8601 with timezone)
- principal: `user`, `user_id`, `device_id`, `host`
- process: `process_name`, `process_path`, `process_sha256`, `parent_process_*`
- network: `src_ip`, `dst_ip`, `dst_port`, `dns_qname`, `tls_sni`, `http_host`, `ja3`, `ja4`, `cert_sha256`
- cloud: `tenant_id`, `account_id`, `app_id`, `resource`, `api_operation`

If platform fields differ materially, include a `field-mapping.md` in the pack or vendor folder.

## Evidence-first outputs

Detections should support defensible evidence:
- include query output fields that can be exported (JSON/CSV)
- include context to explain why an event is suspicious
- prefer outputs that preserve joinable identifiers (host, user, process, dest, time)

If you bundle detections as releases, include:
- versioned zip(s)
- `SHA256SUMS.txt`
- brief release notes

## Safety and publication constraints

This repo is defensive:
- do not include customer identifiers or sensitive environment data
- sanitize samples and screenshots (tenant IDs, emails, hostnames, IPs where sensitive)
- avoid publishing weaponized exploitation steps
- keep detections focused on hardening, validation, and detection engineering

## Contribution checklist

Before opening a PR for detections:
- [ ] correct placement (`vendor-packs/` or `sigma/suricata/yara`)
- [ ] pack README present (if applicable)
- [ ] vendor README present with deploy + tuning + validation steps
- [ ] telemetry prerequisites and required fields documented
- [ ] tuning guidance included (FP discriminators)
- [ ] examples/samples sanitized (no secrets, no identifiers)
- [ ] links added to relevant `research/` write-ups and/or `projects/` tools
