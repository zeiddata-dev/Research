# Zeid Data AI Telemetry Event Schema

This schema is designed for **gateway level AI logging**. You can log more, but do not log less.

## Why these fields exist

- `system_id` and `request_id`: joins, investigations, and evidence
- `model`: pin behavior changes to versions
- `actor`: identity and basic context
- `prompt` and `output`: hashes and classifications instead of raw text by default
- `policy`: allow block redact review plus guardrail reasons
- `tools` and `retrieval`: high risk surfaces, log them
- `metrics`: latency and cost for denial of wallet detection

## Storage guidance

Default posture:
- store raw prompts only when explicitly required
- prefer hashes plus structured classifications
- protect logs like sensitive data, because they are

See the JSON schema: `zeid_data_ai_event_schema.json`.
