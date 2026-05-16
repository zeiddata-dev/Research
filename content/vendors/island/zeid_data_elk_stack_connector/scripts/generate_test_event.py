#!/usr/bin/env python3
"""Generate a fresh sample Island event JSON."""

import json
from datetime import datetime, timezone

evt = {
  "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
  "action": "navigation",
  "user": "analyst@example.com",
  "url": "https://portal.internal.example/login",
  "device": {"id": "DEV-98765", "posture": "verified"},
  "policy": {"name": "App Access - Internal Portal", "decision": "allowed"},
  "source": {"ip": "198.51.100.22"}
}

print(json.dumps(evt, indent=2))
