# Evidence First AI Governance
## A pragmatic implementation guide for NIST AI RMF 1.0 (and GenAI reality)

**Zeid Data Research Lab**  
Version: 0.1  
Date: 2026-02-19

> Disclaimer: This is technical guidance, not legal advice. Also not therapy. 🙂

---

## Executive summary

Most AI governance programs fail for the same reason most security programs fail:
they optimize for **documents** instead of **systems**.

NIST AI RMF 1.0 is intentionally flexible. That is great, until you try to run it.
This paper translates the framework into a practical operating model:

- A small set of controls that map cleanly to **Govern, Map, Measure, Manage**
- A telemetry schema you can pipe into a SIEM
- Evidence bundles you can generate on demand

If you can not prove it, you can not govern it.

---

## 1. Threat model: what can go wrong (and usually does)

AI systems introduce classic software risks plus a few new favorites:

### Data and privacy
- sensitive data leakage through prompts, outputs, logs, or retrieval
- training or tuning on data you did not have rights to use

### Security
- prompt injection and tool abuse
- indirect injection through retrieved content
- model endpoint abuse: scraping, brute forcing, denial of wallet

### Reliability and trust
- hallucinations that look confident
- drift when data, prompts, or policies change
- inconsistent refusal behavior

### Legal and business risk
- IP contamination
- untracked vendor model updates
- opaque decision making for high impact use cases

NIST published a GenAI profile (NIST AI 600-1) as a companion for these generative risks.
Use it as your “yes, we actually use LLMs” appendix.

---

## 2. The Evidence First operating model

### 2.1 Three artifacts that make governance real

1) **AI system record (system card)**
- what the system does
- where it runs
- who owns it
- what data it touches
- what tests it must pass

2) **AI telemetry**
- structured event logs for usage, policy decisions, and outcomes
- enough context to investigate incidents without storing raw secrets forever

3) **Evidence bundle**
- a zip with curated artifacts plus a hash manifest
- repeatable, timestamped, and explainable

Everything else is optional garnish.

### 2.2 Roles (keep it small)

- **Business owner**: owns the risk decision
- **Model steward**: owns evaluation, thresholds, drift response
- **Security**: owns access control, logging, incident response
- **Privacy / legal**: owns data use constraints
- **Platform**: owns gateways, pipelines, uptime

Committees are fine. Ownership is better.

---

## 3. Translating NIST AI RMF into controls you can implement

NIST AI RMF is organized into four functions:

### Govern
You need:
- policy, risk appetite, and accountabilities
- inventory coverage and approval workflow
- incident playbooks and escalation paths

### Map
You need:
- use case definition and impact tier
- data lineage and data rights
- threat model and dependency map

### Measure
You need:
- test suites: quality, safety, robustness
- metrics: drift, hallucination indicators, guardrail hit rates
- evaluation cadence and change triggers

### Manage
You need:
- mitigation actions tied to measured signals
- rollback plans and kill switches
- vendor management and change controls

This pack includes a control matrix you can adopt and expand.

---

## 4. Telemetry: the one thing everyone forgets

If you do not log it, you can not monitor it.
If you can not monitor it, you will learn about failures from screenshots.

Minimum viable telemetry should capture:
- actor, model, and system identifiers
- policy decisions and guardrail outcomes
- tool calls and retrieval sources (high risk area)
- classification results (PII, secrets, toxicity, etc)
- errors, latency, and cost

This pack includes `zeid_data_ai_event_schema.json` plus sample parsing configs.

---

## 5. Evidence bundles: how to survive audits and incidents

A strong evidence bundle is:
- curated (no dump everything)
- hashed (tamper evident)
- timestamped (what was true when)
- readable (README, manifests, summaries)

Include:
- system cards and approvals
- evaluation reports and test results
- monitoring snapshots and threshold definitions
- incident records and postmortems

This pack includes a script that generates a bundle and a SHA256 manifest.

---

## 6. Implementation plan (30 days, boring on purpose)

### Week 1: Govern + Map foundations
- create inventory, owners, impact tiers
- define gateway pattern
- pick telemetry schema

### Week 2: Logging and pipelines
- instrument gateway
- ship JSON events to SIEM
- validate events against schema

### Week 3: Measure
- build evaluation harness per system
- define thresholds and change triggers
- schedule recurring checks

### Week 4: Manage and evidence
- run a tabletop incident
- generate evidence bundle
- produce a control coverage report

If you can do this for one system, you can do it for ten.

---

## 7. References (primary sources)

- NIST AI Risk Management Framework (AI RMF 1.0), released Jan 26, 2023  
  https://www.nist.gov/itl/ai-risk-management-framework

- NIST AI RMF Playbook (living resource)  
  https://airc.nist.gov/airmf-resources/playbook/

- NIST AI 600-1: Generative AI Profile (released July 26, 2024)  
  https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

- ISO/IEC 42001:2023 AI management systems  
  https://www.iso.org/standard/42001

- ISO/IEC 23894:2023 AI risk management guidance  
  https://www.iso.org/standard/77304.html
