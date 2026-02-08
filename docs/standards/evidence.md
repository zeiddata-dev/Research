# Evidence Standards

This repo is evidence-first. If a tool or pack claims “audit-ready,” it should help produce outputs that are clear, repeatable, and defensible.

## What counts as good evidence
Evidence is good when it is:
- Deterministic: same input + same config equals same output
- Traceable: you can tell what ran, when, and with what settings
- Exportable: easy to save and share (JSON/CSV/MD/PDF as needed)
- Readable: a human can understand it without guessing

## Minimum requirements (tools and packs)
Every module should include:
1) README Quickstart
   - how to run it
   - what it produces
   - where outputs go

2) Captured context
   - tool name and version
   - run timestamp
   - input source(s)
   - config used (or a config hash)

3) Stable outputs
   - consistent file names and schema
   - machine-friendly format (usually JSON)
   - optional human summary (Markdown)

## Recommended output structure
Use a single folder for run outputs:

reports/
  run-metadata.json
  findings.json
  findings.csv
  summary.md

If you need multiple runs, nest them:

reports/
  2026-02-08T14-32-10Z/
    run-metadata.json
    findings.json
    summary.md

## run-metadata.json (suggested fields)
Keep it small. Suggested fields:
- tool_name
- tool_version
- run_id
- timestamp
- operator (optional)
- inputs (paths, sources, counts)
- config_path (or config_sha256)
- environment (os, python/node version)
- notes (optional)

## Checksums (when sharing artifacts)
If you publish a zip in releases/, include:
- SHA256SUMS.txt

This helps recipients confirm integrity.

## Chain of custody (when needed)
For high-scrutiny environments, include:
- who collected it (name/role or team)
- when collected it (timestamp + timezone)
- where stored it (system/location)
- any transfers (who/when/how)

Use templates under templates/chain-of-custody/ if available.

## Redaction rules
Do not commit secrets or private data.
- sanitize logs (tokens, emails, IPs if sensitive)
- use sample data where possible
- document any redaction in summary.md
