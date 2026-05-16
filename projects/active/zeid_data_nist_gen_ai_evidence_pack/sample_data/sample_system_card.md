# AI System Card: HR Assistant v1 (example)

## 1. Identity
- System name: HR Assistant
- System id: hr_assistant_v1
- Business owner: HR Operations
- Model steward: HR Analytics
- Security owner: Security Engineering
- Data steward: Privacy Office

## 2. Purpose and scope
- Intended use: Draft HR policy summaries and answer common HR questions
- Out of scope use: Employment decisions, performance scoring, medical or legal advice
- User groups: Employees
- Impact tier: Moderate

## 3. Model and architecture
- Model provider: OpenAI
- Model name and version: gpt-4.1-mini (pinned)
- Hosting: vendor API through company gateway
- Tools enabled: none
- Retrieval sources: approved HR handbook content

## 4. Data
- Retrieval data sources: HR handbook, benefits docs
- Data rights basis: internal corporate docs
- Sensitive data types touched: PII possible

## 5. Controls
- Gateway policy checks: PII detection, secrets detection
- Rate limits: yes
- Output filtering: redaction
- Logging enabled: full telemetry schema
- Kill switch path: feature flag off at gateway

## 6. Evaluation and monitoring
- Quality: answer relevance score >= 0.80 on weekly test set
- Safety: prompt injection suite monthly
- Monitoring: guardrail hit rate, refusal rate, drift score

## 7. Change control
- Prompt version: 2026.02
- Policy version: 2026.02
- Approvals: HR Ops + Security

## 8. Incidents and known issues
- None open
