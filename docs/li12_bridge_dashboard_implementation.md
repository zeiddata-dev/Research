# Li-12 Bridge dashboard implementation guide

This guide explains how to implement the Rebecca Bridge “today emotional weather” dashboard with actual project records only.

## What the dashboard expects

The Bridge page does not recursively scan source folders. It uses a strict allowlist-first loader and only scans existing user-data directories such as:

- `data/bot_profiles/`
- `data/journals/`
- `data/journal/`
- `data/memories/`
- `data/memory/`
- `data/chats/`
- `data/messages/`
- `data/telegram/`
- `data/bridge/`
- `data/bridge_digests/`
- `data/imported_sources/`
- `data/uploads/`
- `data/website_intake/`

It deliberately skips root markdown docs, source code, scripts, reports, inventories, archives, backups, service files, and generic logs unless an allowlisted user-data file has an actual chat/journal/memory/bridge shape.

Use the project’s existing normalization/export job to write actual user records under the allowlisted `data/` directories. Do not put prompts, test notes, generated rows, project docs, source snippets, reports, inventories, or maintenance output into these files.

## Minimal safe record contract

Each actual record needs:

- one timestamp field: `timestamp`, `created_at`, `updated_at`, `date`, `datetime`, `ts`, or `time`
- one display-safe text field: `text`, `summary`, `message`, `content`, `title`, `insight`, `excerpt`, `description`, or `body`
- optional type field: `record_type`, `type`, `category`, `kind`, or `source`
- optional safe display identity: `profile`, `user`, `display_name`, `name`, `author`, or `sender`

Example shape, using real records only:

```json
[
  {
    "timestamp": "2026-05-08T09:30:00-05:00",
    "record_type": "journal",
    "profile": "Rebecca",
    "summary": "Actual user-facing summary text from the journal record."
  }
]
```

Do not include backend/internal fields in user-facing cache data. The dashboard sanitizer also removes these if they appear:

- `source_file`
- `record_hash`
- `imported_path`
- `raw`
- `parse_error`
- `privacy_level`
- `private_queue`
- backend/debug/environment fields

## How to wire actual records into the dashboard

1. Locate the existing Li-12 normalizer/exporter that already reads chats, journals, memories, bridge records, and insight records.
2. Make that job write actual user-facing records into the matching allowlisted `data/` directory, such as `data/chats/`, `data/journals/`, `data/memories/`, or `data/bridge/`.
3. Normalize each actual source item into the minimal safe record contract above.
4. Keep backend metadata in backend-only stores, not in the display cache.
5. Start the Streamlit app from the repo root:

```bash
streamlit run li12_unified_dashboard.py
```

6. Open the Bridge page. If no usable actual records exist for the current America/Chicago calendar day, the page must show exactly:

```text
No usable actual records found for today.
```

## How today filtering works

`get_today_bounds()` creates the local start and exclusive end bounds for the current calendar day in `America/Chicago` by default.

`filter_records_for_today()` accepts the already-loaded cached records, parses common timestamp fields defensively, treats naive timestamps as local time, rejects records without valid today timestamps, and returns only records that also have usable display text.

## How the rating works

The rating is deterministic and never calls an LLM.

When there is at least one usable record today, scoring starts at `60` and applies capped signal deltas:

- repair signal: `+8` each, cap `+20`
- stability signal: `+6` each, cap `+18`
- follow-through signal: `+10` each, cap `+20`
- escalation signal: `-10` each, cap `-30`
- open loop or repeated topic: `-7` each, cap `-21`
- late-night intensity: `-8` each, cap `-16`
- over-explaining signal: `-5` each, cap `-15`

The final score is clamped to `0-100`.

Labels:

- `80-100`: Stable
- `60-79`: Repairing
- `40-59`: Heavy
- `20-39`: Tense
- `0-19`: Escalating
- no records: Not enough data

Confidence:

- `high`: 10+ usable evidence records
- `medium`: 4-9 usable evidence records
- `low`: 1-3 usable evidence records
- no data: not enough data

## Validation commands

Run these from the repo root after implementation changes:

```bash
python3 -m py_compile li12_unified_dashboard.py dashboard_data_loader.py dashboard_insights.py dashboard_privacy.py dashboard_components.py
python3 scripts/audit_dashboard_sources.py
```

Expected result:

- `py_compile` exits with status `0`
- audit prints `PASS: dashboard source audit passed`

## Troubleshooting

If the dashboard shows the empty state:

1. Confirm a recognized cache file exists in one of the expected cache directories.
2. Confirm records are actual project records, not prompt text or generated placeholders.
3. Confirm timestamps fall inside today’s America/Chicago calendar day.
4. Confirm each record has at least one usable display text field.
5. Confirm records are not classified as admin, system, backend, debug, or internal records.

If validation fails:

1. Read the exact audit failure message.
2. Remove any `use_container_width` usage from dashboard files.
3. Remove direct rendering references to forbidden backend fields.
4. Keep the exact empty-state string unchanged.
5. Re-run both validation commands.
