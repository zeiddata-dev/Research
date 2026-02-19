# HOWTO: Operationalize NIST AI RMF without turning into a policy goblin

This guide shows how to use this pack as a practical implementation path.

## Step 1: Inventory or it did not happen

Create an AI system inventory and treat it like production infrastructure.
Minimum fields:
- system name
- owner
- model provider (or internal)
- data sources (training, tuning, retrieval)
- user groups
- deployment environment
- impact tier

Use `controls/zeid_data_model_system_card_template.md` as the system record.

## Step 2: Put a gateway in front of AI

Your gateway is where you enforce:
- auth and rate limits
- tenant and user scoping
- input and output policy checks
- tool and retrieval allow lists
- logging

Do not rely on application teams to remember this forever. They will not. 🙂

## Step 3: Log AI like you log production auth

Adopt `logging/zeid_data_ai_event_schema.json`.

At minimum you want:
- who used what model and when
- prompt and output classification results
- policy decisions and guardrail hits
- tool calls and retrieval sources
- errors, latency, cost

Then ship the events to your SIEM.

## Step 4: Measure what matters

For each system, define:
- acceptance criteria (accuracy, hallucination tolerance, refusal behavior)
- safety tests (prompt injection, data leakage)
- monitoring thresholds (drift, guardrail hit rates)

Do this before you roll out to the whole company. Yes, before.

## Step 5: Evidence bundles (audit ready, not audit hopeful)

When someone asks:
"Do we have AI governance?"
you want to answer with a zip file.

Use `scripts/bundle_evidence.py` to generate:
- a curated evidence bundle
- a manifest with SHA256 hashes
- a timestamped package label

Then map evidence back to controls with `scripts/generate_coverage_report.py`.

## Step 6: Make it boring

The best governance program is the one that runs automatically.
- scheduled exports
- automated validations
- dashboards with thresholds
- alerts with owners

If it is exciting, it is probably broken.

## Common pitfalls

- Logging prompts in plain text forever (hello sensitive data)
- No model inventory, only "we use AI in the product"
- Treating evaluations as a one time project
- No owners, only committees

## Support

This pack is a starter. Adapt it to your environment.
If you want a more opinionated version for your stack (Splunk, Elastic, Sentinel, Snowflake), you know where to find us.
