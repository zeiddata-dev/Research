# Zeid Data Research Lab: AI Governance Monitoring Pack (Evidence First Edition)

Welcome to the part of AI governance that actually runs in production.

This pack is a pragmatic implementation starter for **NIST AI RMF 1.0** (Govern, Map, Measure, Manage) with a heavy bias toward:
- **Telemetry you can query**
- **Controls you can prove**
- **Evidence bundles you can hand to auditors without crying**

If your current AI governance program is mostly a slide deck and a vibe, this will feel different. 🙂

## What is inside

- **White paper**
  - `zeid_data_whitepaper_ai_governance.md`
  - `zeid_data_whitepaper_ai_governance.pdf`
- **Control set + templates**
  - `controls/zeid_data_control_matrix.csv`
  - `controls/zeid_data_model_system_card_template.md`
  - `controls/zeid_data_risk_register_template.csv`
  - `controls/zeid_data_vendor_questionnaire.md`
- **Telemetry schema**
  - `logging/zeid_data_ai_event_schema.json`
  - `logging/zeid_data_ai_event_schema.md`
  - Example parsing configs for Splunk and Elastic
- **Scripts**
  - `scripts/validate_events.py` validate JSONL AI events against schema
  - `scripts/bundle_evidence.py` create an evidence bundle with a hash manifest
  - `scripts/generate_coverage_report.py` map evidence files back to controls
- **Sample data**
  - `sample_data/sample_ai_events.jsonl`
  - `sample_data/sample_system_card.md`
  - `sample_data/sample_risk_register.csv`
- **Diagram**
  - `diagrams/zeid_data_ai_governance_architecture.mmd` (Mermaid)

## Quick start (10 minutes)

1) Install deps
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Validate sample telemetry
```bash
python scripts/validate_events.py --schema logging/zeid_data_ai_event_schema.json --events sample_data/sample_ai_events.jsonl
```

3) Build a tiny evidence bundle
```bash
python scripts/bundle_evidence.py --input sample_data --output out/evidence_bundle.zip --label "demo"
```

4) Generate a control coverage report
```bash
python scripts/generate_coverage_report.py --controls controls/zeid_data_control_matrix.csv --evidence out/unpacked_demo --output out/control_coverage.md
```

## Philosophy (aka the part people skip)

AI is software. Software fails. AI fails with extra personality.

The goal is not perfect safety. The goal is:
- known risks
- known controls
- monitored drift
- auditable evidence

## License

See `LICENSE`. Use it, fork it, ship it.
