#!/usr/bin/env bash
set -euo pipefail

SECRET="${ISLAND_SHARED_SECRET:-}"
AUTH_HEADER=()

if [[ -n "$SECRET" ]]; then
  AUTH_HEADER=(-H "Authorization: Bearer $SECRET")
else
  echo "[WARN] ISLAND_SHARED_SECRET is empty; auth check is disabled."
fi

echo "[INFO] Posting sample event to Logstash HTTP input..."
curl -sS -X POST "http://localhost:8080/island"   -H "Content-Type: application/json"   "${AUTH_HEADER[@]}"   --data-binary @examples/island_event_sample.json | cat

echo
echo "[INFO] Done. Now open Kibana -> Discover and look for event.module:island"
