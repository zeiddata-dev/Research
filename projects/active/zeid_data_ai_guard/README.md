<!-- ZEID DATA README HERO START -->
![Zeid Data projects banner](../../../assets/banners/readme/projects.png)

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../.."><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data — AIGO (AI Governance Evidence Toolkit)

AIGO is a lightweight, dependency-light CLI that helps teams **operationalize AI governance as evidence**:

- **Model/system inventory** (registry)
- **Eval gates** (policy-driven checks over prompt/response pairs)
- **Telemetry normalization** (JSONL events → stable evidence schema)
- **Evidence bundles** (hash-manifest + audit pack zip)

This is intentionally **offline / deterministic**: it does not call any LLM APIs. It evaluates captured outputs and produces auditable artifacts.

## What this program helps you do
### 1) Inventory (Model Registry)
- Track model IDs, versions, owners, environments, endpoints
- Track risk tier + data classes + tool surface area
- Record approvals (who approved what, when)

### 2) Policy as an evidence contract
Policies are JSON (no dependency on YAML). The baseline policy supports:
- logging settings (hash/store raw prompt/response)
- tool allowlists
- sensitive pattern detection
- evaluation gates

### 3) Eval gates (CI friendly)
Provide a JSONL suite of captured interactions:

```json
{"case_id":"...","prompt":"...","response":"..."}
```

AIGO evaluates each case and fails CI (exit code `2`) if the suite violates gates.

### 4) Telemetry normalization
Convert app/gateway logs to a stable schema for audit evidence (with prompt/response hashing by default).

### 5) Evidence bundles + audit packs
Package:
- registry
- policy
- eval reports (JSON + HTML)
- telemetry exports (raw + normalized)

All files are hashed and written to a `manifest.json` to support chain-of-custody.

## Quickstart
```bash
# 1) Initialize a workspace
python aigo.py init --workspace .

# 2) Add a model record
python aigo.py model add \
  --registry ./registry.json \
  --name "gpt-4.1-mini" \
  --vendor "OpenAI" \
  --environment "prod" \
  --owner "ml-platform" \
  --version "2026-01-17" \
  --artifact-sha256 "<sha256-of-your-artifact>" \
  --tools search kb.lookup

# 3) Run eval gates
python aigo.py eval run \
  --suite ./sample_data/eval_suite.jsonl \
  --policy ./policy.json \
  --model-id "m-demo" \
  --out-json ./out/eval_report.json \
  --out-html ./out/eval_report.html

# 4) Normalize telemetry
python aigo.py telemetry normalize \
  --input ./sample_data/events.jsonl \
  --output ./out/normalized_events.jsonl \
  --policy ./policy.json \
  --summary-json ./out/telemetry_summary.json

# 5) Build an evidence bundle + zip
python aigo.py evidence pack \
  --out-dir ./evidence/bundle \
  --zip ./evidence/audit_pack.zip \
  --registry ./registry.json \
  --policy ./policy.json \
  --eval-json ./out/eval_report.json \
  --eval-html ./out/eval_report.html \
  --raw-events ./sample_data/events.jsonl \
  --norm-events ./out/normalized_events.jsonl
```

## Notes / Extensions
AIGO is meant to be integrated at the **app/gateway layer**:
- attach *structured* citations to responses
- log tool calls + auth context
- emit a JSON event per request

If you want, I can extend this into:
- SLSA-style attestation for model + prompt template builds
- RAG corpus lineage manifests (dataset IDs, classification tags, retention)
- policy decision engine hooks (allow/deny + reason codes)
- SOC 2 / ISO 27001 / NIST mappings exported as evidence

**zeiddata.com**
