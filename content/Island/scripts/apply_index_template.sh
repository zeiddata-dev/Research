#!/usr/bin/env bash
set -euo pipefail
echo "[INFO] Applying index template to Elasticsearch (no auth assumed in this compose)..."
curl -sS -X PUT "http://localhost:9200/_index_template/island-audits-template"   -H "Content-Type: application/json"   --data-binary @elastic/index-template-island.json | jq .
echo "[INFO] Done."
