#!/usr/bin/env python3
"""
validate_events.py
Validate JSONL AI telemetry events against a JSON schema.

Usage:
  python scripts/validate_events.py --schema logging/zeid_data_ai_event_schema.json --events sample_data/sample_ai_events.jsonl
"""
import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="Path to JSON schema")
    ap.add_argument("--events", required=True, help="Path to JSONL events file")
    ap.add_argument("--max-errors", type=int, default=50, help="Stop after this many errors")
    args = ap.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    total = 0
    invalid = 0

    p = Path(args.events)
    for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        total += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            invalid += 1
            print(f"[line {line_no}] JSON decode error: {e}")
            if invalid >= args.max_errors:
                break
            continue

        errors = sorted(validator.iter_errors(obj), key=lambda e: e.path)
        if errors:
            invalid += 1
            print(f"[line {line_no}] invalid event")
            for err in errors[:10]:
                path = ".".join([str(x) for x in err.path]) or "<root>"
                print(f"  - {path}: {err.message}")
            if invalid >= args.max_errors:
                break

    ok = total - invalid
    print("\nSummary")
    print(f"  total:   {total}")
    print(f"  valid:   {ok}")
    print(f"  invalid: {invalid}")

    return 0 if invalid == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
