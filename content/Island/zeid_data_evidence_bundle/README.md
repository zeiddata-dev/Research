# Zeid Data Island Evidence Bundle Kit

This repo is a tiny kit for generating **audit-ready evidence bundles** from an Island Enterprise Browser tenant.

It’s built for boring but important problems:
- prove what policies existed
- prove what changed, when, and by whom (where the API allows it)
- export activity logs in a SIEM-friendly format
- package it all into a bundle with a manifest + hashes (so nobody can say you “hand-edited” the receipts)

## What you get
- **Collectors** that pull Island API resources into newline-delimited JSON (NDJSON / JSONL)
- A **bundle builder** that packages artifacts into a timestamped bundle with:
  - `manifest.json` (inventory + SHA256 per file)
  - `chain_of_custody.md` (custodian notes + collection details)
  - lightweight **reports** (summary counts + optional drift compare)

## Assumptions
- You have an Island admin API key (Management Console → Settings → API).
- You know your Island API base URL.
  - US commonly: `https://management.island.io/api/external/v1/`
  - EU commonly: `https://eu.management.island.io/api/external/v1/`
  These URLs are widely referenced in third-party integration guides, but confirm in your tenant.

## Quick start
1) Create a venv and install deps:
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r zeid_datapip_requirements.txt
```

2) Copy config and set your API key:
```bash
cp zeid_data_config.example.yaml zeid_data_config.yaml
cp zeid_data_env.example .env
# edit .env and zeid_data_config.yaml
```

3) Collect artifacts:
```bash
python zeid_data_collect.py --config zeid_data_config.yaml --out out/collected
```

4) Build an evidence bundle zip:
```bash
python zeid_data_make_bundle.py --in out/collected --out out/bundles \
  --case-id "CASE-001" --custodian "Your Name"
```

## Output format
Collection produces:
- `out/collected/collection_metadata.json`
- `out/collected/data/*.jsonl` (one file per endpoint)

Bundle builder produces:
- `out/bundles/evidence_bundle_CASE-001_YYYYmmddTHHMMSSZ.zip`
- inside: `data/`, `reports/`, `manifest.json`, `chain_of_custody.md`

## Why NDJSON/JSONL
Because logs want to be logs. Every line is one event/object. Logstash, Splunk, and basically any grown-up pipeline will ingest it without drama.

## Security notes
- Treat the API key like it’s a production password.
- Don’t store keys in Git.
- Prefer running collection on a trusted admin workstation.
- If you need “court-grade” handling, do this on a dedicated machine, record hashes, and keep the raw outputs immutable.

## Limitations (aka reality)
Island API endpoints and pagination patterns can vary by tenant/version.
This kit is intentionally configurable: you define the endpoints you want in YAML.

If an endpoint is asynchronous (export jobs), you’ll need to configure it in `zeid_data_config.yaml` using the “job” pattern described in HOWTO.

## Version
0.1.0 (2026-02-16T15:32:45Z)
