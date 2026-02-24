# HOWTO: Use `zeid_data_regex_safety_tester.py`

## What it does

This script provides:
- heuristic checks for common regex risk smells
- toy performance benchmarking for potential backtracking behavior
- sample probes for logic review (anchors/grouping/domain patterns)

It is a **defensive review helper**, not a proof system.

## Quick Start

### 1) Run the built-in demo set
```bash
python zeid_data_regex_safety_tester.py --demo
```

### 2) Test a single pattern
```bash
python zeid_data_regex_safety_tester.py --pattern "^(a+)+$"
```

### 3) Test with custom toy samples
```bash
python zeid_data_regex_safety_tester.py --pattern "^(?:admin|root)$" --sample "admin" --sample "admin123" --sample "root"
```

### 4) Adjust timeout and lengths
```bash
python zeid_data_regex_safety_tester.py --pattern "^(a+)+$" --timeout-ms 50 --max-len 24
```

## Output Overview

The script reports:
- pattern
- heuristic warnings (if any)
- benchmark timings by input length
- whether a timeout occurred
- basic sample match results

## How to Use in Team Reviews

- Run it on regex used in:
  - auth / identity flows
  - redirect validation
  - URL/domain allowlists
  - request validation
  - SIEM parsers and detection rules
- Add adversarial toy samples to CI
- Watch for timing growth and logical false positives

## Important Limitations

- Python `re` engine behavior is engine-specific; other languages/engines may behave differently
- Timing results vary by hardware and runtime
- Heuristics can miss risks or flag false positives
- Use parser-based validation for structured trust decisions where possible
