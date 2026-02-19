# Zeid Data AI Control Matrix (starter)

This is a starter set. Add controls as you learn what your AI systems actually do.

| Control ID | Function | Domain | Statement | Evidence | Owner | Freq |
|---|---|---|---|---|---|---|
| ZD-AI-GOV-01 | Govern | Accountability | Assign a business owner and model steward for every AI system. | System card with named owners; approval record | AI Program Lead | Per system |
| ZD-AI-GOV-02 | Govern | Inventory | Maintain an AI system inventory and keep it current. | Inventory export; change log | Platform | Weekly |
| ZD-AI-GOV-03 | Govern | Policy | Publish minimum AI use policy and acceptable use rules. | Policy doc; training acknowledgment | Privacy | Quarterly |
| ZD-AI-GOV-04 | Govern | Change Control | Document vendor model updates and internal prompt or policy changes. | Change ticket; release notes | Platform | Per change |
| ZD-AI-MAP-01 | Map | Use Case | Define intended use, out of scope use, and impact tier. | System card section; impact assessment | Product | Per system |
| ZD-AI-MAP-02 | Map | Data Rights | Document data sources and rights for training, tuning, retrieval. | Data lineage doc; approvals | Privacy | Per system |
| ZD-AI-MAP-03 | Map | Threat Model | Threat model prompt injection, tool abuse, and retrieval risks. | Threat model doc; mitigations | Security | Per system |
| ZD-AI-MEAS-01 | Measure | Quality | Define measurable acceptance criteria for task quality. | Eval report; benchmarks | Model Steward | Monthly |
| ZD-AI-MEAS-02 | Measure | Safety | Run red team prompts for injection and data leakage. | Test suite output; findings | Security | Monthly |
| ZD-AI-MEAS-03 | Measure | Monitoring | Monitor drift and guardrail hit rates over time. | Dashboard snapshot; alerts | Platform | Daily |
| ZD-AI-MEAS-04 | Measure | Logging Validation | Validate telemetry conforms to schema. | Validation report | Platform | Daily |
| ZD-AI-MAN-01 | Manage | Mitigation | Define response actions for threshold breaches. | Runbooks; tickets | Security | Per event |
| ZD-AI-MAN-02 | Manage | Kill Switch | Implement model or feature disablement path. | Config; test evidence | Platform | Quarterly |
| ZD-AI-MAN-03 | Manage | Evidence Bundle | Generate audit ready evidence bundles on demand. | Bundle zip; manifest hashes | GRC | Quarterly |
| ZD-AI-VEND-01 | Govern | Vendor | Assess model vendors for security, privacy, and update controls. | Vendor questionnaire; contract clauses | Procurement | Annual |
