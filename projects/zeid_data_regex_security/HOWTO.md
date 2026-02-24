# HOWTO: Use `zeid_data_regex_safety_tester.py` 🧰🧪

## What it does

This script gives you:

* heuristic checks for common regex risk smells
* toy performance benchmarking for possible backtracking behavior
* sample probes for logic review (anchors, grouping, domain patterns)

It is a **defensive review helper**, not a proof system.
So think “useful flashlight,” not “formal verification wizard.” 🔦

## Quick Start 🚀

### 1) Run the built in demo set

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

## Output Overview 📋

The script reports:

* pattern
* heuristic warnings (if any)
* benchmark timings by input length
* whether a timeout occurred
* basic sample match results

Basically, it helps you spot “this seems fine” regex that is quietly preparing a bad day. 😬

## How to Use in Team Reviews 👀

Run it on regex used in:

* auth / identity flows
* redirect validation
* URL/domain allowlists
* request validation
* SIEM parsers and detection rules

Then:

* add adversarial toy samples to CI
* watch for timing growth
* check for logical false positives and false negatives

Because matching the happy path is easy. Production specializes in the other paths.

## Important Limitations ⚠️

* Python `re` behavior is engine specific; other languages and engines may behave differently
* Timing results vary by hardware and runtime
* Heuristics can miss risks or flag false positives
* Use parser based validation for structured trust decisions where possible

This tool helps you review regex.
It does not magically make unsafe patterns safe just because they passed one quick test. 🤖
