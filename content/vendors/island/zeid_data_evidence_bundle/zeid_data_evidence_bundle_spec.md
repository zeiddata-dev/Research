# Evidence bundle spec (Zeid Data)

This is the minimum bundle structure this kit targets.

## Required
- `manifest.json`
  - inventory of every file in the bundle
  - SHA256 per file
  - bundle metadata (case_id, custodian, created_at, tool version)
- `chain_of_custody.md`
  - who created it
  - when (UTC)
  - where (machine / environment details if you want to be extra)
  - how (command line + config reference)
- `data/`
  - raw exports in JSONL/NDJSON/CSV
- `reports/summary.md`
  - simple counts, time range, and endpoint coverage

## Strongly recommended
- `collection_metadata.json` copied from collection run
- optional `reports/policy_drift.md` if baseline compare available
- include the exact config file used (if allowed) as `config_used.yaml`

## Integrity rules
- Only generate hashes after all files are written
- Preserve bundle zip as immutable
- If you transfer it, compute SHA256 of the zip and record it in your matter notes
