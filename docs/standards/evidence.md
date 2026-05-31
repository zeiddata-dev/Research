# Evidence Standards

This repo is evidence-first. If a tool, detection, report, workbook, or research note makes a claim, the supporting artifact should be findable and reviewable.

## What good evidence looks like

Good evidence is:

- **Traceable:** the reader can identify inputs, source files, data sources, queries, commands, or references.
- **Repeatable:** another reviewer can rerun the command, query, or workflow in a controlled environment.
- **Bounded:** the document says what is covered and what is not covered.
- **Exportable:** outputs can be saved as JSON, CSV, Markdown, screenshots, bundles, or platform-native exports.
- **Public-safe:** examples are sanitized and do not expose private data.

## Minimum evidence requirements

Every artifact that claims to detect, validate, audit, or summarize should include:

1. **Purpose**
   - What problem it solves.
   - Who should use it.

2. **Inputs**
   - Required logs, tables, files, APIs, configs, or sample data.
   - Minimum permissions.
   - Expected time range or scope.

3. **Method**
   - Query, rule, script, or procedure used.
   - Any thresholds or assumptions.
   - Any allowlists or exclusions.

4. **Outputs**
   - Output file names or schemas.
   - Example fields.
   - How to read pass/fail or result states.

5. **Validation**
   - How to test it safely.
   - Expected result for a known-good sample.
   - Known false positives or failure modes.

6. **Limits**
   - What the artifact does not prove.
   - What data gaps could invalidate the result.

## Suggested output structure

For tools and scripts:

```text
reports/
  run-metadata.json
  findings.json
  findings.csv
  summary.md
```

For repeated runs:

```text
reports/
  2026-05-31T17-00-00Z/
    run-metadata.json
    findings.json
    summary.md
```

## Suggested run metadata

```json
{
  "tool_name": "example-tool",
  "tool_version": "0.1.0",
  "run_id": "2026-05-31T17-00-00Z-example-tool",
  "generated_at": "2026-05-31T17:00:00Z",
  "input_sources": ["example.jsonl"],
  "config_sha256": "optional",
  "output_files": ["findings.json", "summary.md"],
  "assumptions": ["sample data only"],
  "limitations": ["does not prove absence of activity"]
}
```

## Evidence language

Use precise language.

Preferred:

- `Observed in the provided sample.`
- `Detected when this field is present.`
- `Not evaluated because source data was missing.`
- `Evidence missing.`
- `Manual review required.`

Avoid:

- `Confirmed safe.`
- `Fully protected.`
- `Complete coverage.`
- `Production ready.`
- `High risk` without scoring criteria and evidence.

## Redaction rules

Do not commit:

- secrets, tokens, API keys, passwords, cookies, or session data
- private customer logs
- personal data that is not explicitly public-safe
- private URLs or infrastructure details
- exploit-ready material that enables unauthorized activity

Use synthetic examples or sanitized samples. If redaction was performed, say what category of data was removed.

## Review checklist

Before publishing a doc or artifact, check:

- [ ] Purpose is clear.
- [ ] Inputs are listed.
- [ ] Outputs are listed.
- [ ] Validation or test path is included.
- [ ] Assumptions are explicit.
- [ ] Limits are explicit.
- [ ] Links are valid.
- [ ] Examples are sanitized.
- [ ] Claims are tied to evidence or clearly marked as missing.
