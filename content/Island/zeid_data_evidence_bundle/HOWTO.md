# HOWTO: Generate Island reporting and evidence bundles

This is the step-by-step playbook. If you want vibes, try candles. If you want receipts, keep reading.

---

## 0) Prereqs
- Python 3.10+ recommended
- An Island admin API key (Management Console → Settings → API)
- Your Island Management API base URL (US/EU tenant)
- Network access to the Island management API

---

## 1) Configure
### 1.1 Create local config
Copy the example file and edit:
```bash
cp zeid_data_config.example.yaml zeid_data_config.yaml
```

Key fields you should set:
- `base_url`: your Island API base URL (ends with `/api/external/v1/` usually)
- `auth`:
  - `api_key_env`: environment variable name holding your API key (default `ISLAND_API_KEY`)
  - `header`: the HTTP header name used for the key (default `Authorization`)
  - `prefix`: header prefix (default `Bearer`)

**If your tenant uses a different header**, update these values. This kit supports either:
- `Authorization: Bearer <key>`
- or `x-api-key: <key>` style setups (set `header: x-api-key` and `prefix: ""`)

### 1.2 Set environment
Copy the env example:
```bash
cp zeid_data_env.example .env
```

Then set:
- `ISLAND_API_KEY=...`

On Linux/macOS:
```bash
set -a
source .env
set +a
```

On Windows PowerShell:
```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match "^(\w+)=(.*)$") { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process") }
}
```

---

## 2) Choose what to collect
In `zeid_data_config.yaml`, define endpoints to pull. Example entries:
- users
- devices
- policies
- logs (often time-filtered)

Each endpoint entry supports:
- `name`: logical label
- `path`: relative path appended to base_url
- `params`: query params (dict)
- `output`: output file path under the collection folder (recommended: `data/...jsonl`)
- `item_path`: optional JSON pointer-ish traversal for where the list of items lives in responses

---

## 3) Collect
```bash
python zeid_data_collect.py --config zeid_data_config.yaml --out out/collected
```

This writes:
- `collection_metadata.json` with counts, timings, and errors
- `data/*.jsonl` raw exports

If your logs endpoint supports time filters, set:
- `logs_start` and `logs_end` in config (ISO8601)
- or pass `--since-hours 24` to collect recent activity

---

## 4) Build the evidence bundle
```bash
python zeid_data_make_bundle.py --in out/collected --out out/bundles --case-id "CASE-001" --custodian "Your Name"
```

The output zip contains:
- `manifest.json` listing every file + SHA256 checksum
- `chain_of_custody.md` with who/when/where/how
- `reports/summary.md` basic counts and timing
- `data/` the raw NDJSON exports

---

## 5) Optional: policy drift compare
If you have a previous collection or bundle directory, you can compare:
```bash
python zeid_data_make_bundle.py --in out/collected --out out/bundles \
  --case-id "CASE-001" --custodian "Your Name" \
  --baseline out/previous_collected
```

The report will:
- hash policy objects (stable JSON canonicalization)
- list changed/added/removed items (best effort)

---

## 6) Optional: async export job pattern
Some APIs don’t hand you a giant CSV/JSON in one response. They make you:
1) create export job
2) poll status
3) download result from a URL

If Island uses that pattern for any endpoints you need, configure an endpoint with:
- `mode: export_job`
- `job_create_path`
- `job_status_path`
- `job_result_field` (where the download URL lives)

See `zeid_data_config.example.yaml` for a template.

---

## 7) Handing to counsel / auditors
Send:
- the evidence bundle zip
- the exact config file used
- the command line you ran
- (optional but strong) a screenshot of the terminal showing the SHA256 of the final zip

Because “trust me bro” is not a control.
