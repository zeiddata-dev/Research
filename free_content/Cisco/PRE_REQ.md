## Requirements
You’ll need:

- Cisco logs forwarded to your log platform (SIEM, data lake, or log pipeline)
- Time synchronization (NTP) across log sources
- A place to store tuning artifacts (allowlists, known-good destinations, service accounts)

Optional but recommended:

- Asset inventory or CMDB enrichment (hostnames, owners, environment tags)
- DNS enrichment (domain age, registrar, reputation feeds where permitted)

## Quick start
1. Confirm you are ingesting Cisco telemetry and can query it.
2. Start with the “low risk, high signal” detections:
   - Rare outbound domain / rare destination
   - High NXDOMAIN bursts
   - Repeated auth failures followed by a success
3. Run each detection in “report-only” mode for 7–14 days.
4. Apply the tuning guidance in `tuning/`:
   - Add known business SaaS domains
   - Exclude approved scanners and management subnets
   - Baseline service accounts and admin jump hosts
5. Promote to alerting once false positives are under control.

## Data notes and field mapping
Cisco products log similar concepts using different fields depending on product and export method. In `data_dictionary/`, keep a short mapping for your environment, for example:

- Source IP / user / device identity
- Destination IP / destination domain / SNI
- Action (allowed, blocked, proxied)
- Policy name / rule name
- Event category and severity

If your pipeline normalizes to a common schema (ECS, CIM, OCSF, custom), document that here.

## Tuning philosophy
This pack assumes an evidence-first workflow:

- Start broad, observe, then narrow
- Prefer explainable filters over opaque scoring
- Capture “why this fired” in the alert output (domain, first seen time, count, baseline delta)
- Keep allowlists explicit and reviewable

## Validation and testing
Use `testing/` for repeatable checks:

- Known benign test events (approved SaaS, internal resolvers, admin logins)
- Known suspicious simulations where allowed (e.g., DNS to a canary domain you control)
- Regression checks after pipeline or parser changes

## False positives you should expect
These detections can surface legitimate activity, especially early on:

- New SaaS rollouts
- Browser updates and CDN shifts
- Remote work and travel
- Security tools that perform scanning or reputation checks

This is normal. Treat the first tuning cycle as baselining.

## Limitations
- Some Cisco products require specific logging levels or export settings to capture fields used by higher-fidelity detections.
- DNS-only environments can detect patterns, but may not identify the exact process/user without additional telemetry.
- NetFlow can highlight behavior, but often needs enrichment to be actionable.

## Contributing
If you improve a rule or add a new data source mapping:

1. Keep detections readable and documented.
2. Include a short “why it matters” note and expected false positives.
3. Add a test query or validation step.

## License
Unless otherwise noted, content in this folder is released under the repository’s license. If your repo uses MIT or Apache-2.0, this pack follows that.

## Disclaimer
This content is provided as-is. You are responsible for evaluating detections, ensuring compliance with internal policies, and validating impact before enabling alerting in production.

## Contact
Zeid Data Research Labs
- Issues and requests: use GitHub Issues in this repo
- If you want a vendor-specific version (Umbrella-only, Firewall-only, Duo-only), create an issue describing your log source and schema.
