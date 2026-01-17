███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║

# Zeid Data - Copper Hang Back...
# HOWTO — Zeid Data AIGO

This guide shows how to use AIGO to produce **audit-ready AI governance artifacts**.

## 1) Set up a workspace
```bash
python aigo.py init --workspace ./aigo_ws
```
Creates:
- `registry.json` — model/system inventory
- `policy.json` — governance policy baseline
- `out/` — generated reports
- `evidence/` — evidence bundles

## 2) Model Registry (inventory + approvals)
### Add a model
```bash
python aigo.py model add \
  --registry ./aigo_ws/registry.json \
  --name "prod-rag-assistant" \
  --vendor "OpenAI" \
  --environment prod \
  --owner "ml-platform" \
  --version "2026-01-17" \
  --artifact-sha256 "<sha256>" \
  --tools search kb.lookup ticket.create
```

### Approve a model
```bash
python aigo.py model approve --registry ./aigo_ws/registry.json m-<id> --approver "security@zeiddata" --comment "Eval gates passed"
```

## 3) Eval gates (offline, deterministic)
AIGO evaluates captured prompt/response pairs and enforces gates from `policy.json`.

Suite format: JSONL objects with:
- `case_id` (optional)
- `prompt` (required)
- `response` (required)
- `tags` (optional)

Run:
```bash
python aigo.py eval run \
  --suite ./aigo_ws/suites/regression.jsonl \
  --policy ./aigo_ws/policy.json \
  --model-id m-<id> \
  --out-json ./aigo_ws/out/eval_report.json \
  --out-html ./aigo_ws/out/eval_report.html
```

**Exit codes**
- `0` = pass
- `2` = failed gates (CI should fail)

## 4) Telemetry normalization
AIGO consumes **your** JSONL events (from app, gateway, proxy, etc.) and outputs a normalized schema.

Minimal input fields (best-effort):
- `ts_utc`, `model_id`, `environment`
- `actor`, `session_id`, `request_id`
- `prompt`, `response`
- `tool_calls` (list of `{name,outcome,latency_ms}`)
- `policy_decision`, `rules_hit`

Run:
```bash
python aigo.py telemetry normalize \
  --input ./aigo_ws/raw/events.jsonl \
  --output ./aigo_ws/out/normalized_events.jsonl \
  --policy ./aigo_ws/policy.json
```

### Raw content storage (privacy note)
By default, the baseline policy stores only hashes for prompts/responses.

If you enable `logging.store_raw_content=true`, provide `--raw-dir`:
```bash
python aigo.py telemetry normalize --input ... --output ... --policy ... --raw-dir ./aigo_ws/out/raw
```

## 5) Evidence bundle + audit pack
Bundle the artifacts you want to hand to an auditor:
```bash
python aigo.py evidence pack \
  --out-dir ./aigo_ws/evidence/bundle \
  --zip ./aigo_ws/evidence/audit_pack.zip \
  --registry ./aigo_ws/registry.json \
  --policy ./aigo_ws/policy.json \
  --eval-json ./aigo_ws/out/eval_report.json \
  --eval-html ./aigo_ws/out/eval_report.html \
  --raw-events ./aigo_ws/raw/events.jsonl \
  --norm-events ./aigo_ws/out/normalized_events.jsonl
```

The bundle includes:
- `manifest.json` — sha256 for every file (chain-of-custody)
- `narrative.md` — human-readable summary of what’s inside

## Suggested next steps (production-grade)
- Add a **model build attestation** (artifact hash signed by CI)
- Add **RAG corpus manifests** (dataset IDs + classification + retention)
- Enforce **tool allowlists** at runtime (not only in telemetry)
- Implement **structured citations** (metadata, not heuristic text parsing)
- Map artifacts to your frameworks (SOC 2 / ISO 27001 / NIST) as evidence

**zeiddata.com**
