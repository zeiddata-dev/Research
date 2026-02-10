# Zeid Data — SonarCloud Content (CI Merge Gating, Deterministic Quality Gates, Evidence Output)

This directory contains Zeid Data SonarCloud-specific integration content engineered to convert SonarCloud analysis into deterministic, CI-enforced merge decisions. The primary goal is to treat SonarCloud Quality Gates as a hard control surface: every pipeline run binds Quality Gate evaluation to a specific analysis snapshot (analysisId) and returns machine-verifiable exit codes suitable for branch protection, release controls, and evidence retention.

---

## SonarCloud-Specific Assumptions and Constraints

SonarCloud is hosted and multi-tenant. As a result, integrations must be built with:
- Strict token handling (CI secret injection only; never log tokens).
- Explicit, stable base URL usage (SonarCloud default is https://sonarcloud.io).
- Reliable post-scan synchronization: scanner completion does not guarantee the Compute Engine (CE) has finished processing the analysis.
- Correct branch/PR attribution: ensure scanners supply branch/PR metadata so SonarCloud associates the analysis to the intended context.

Key consequence: merge gating should bind to the analysisId returned by CE completion, not to broad project queries, to avoid timing and attribution ambiguity.

---

## SonarCloud Analysis Lifecycle (CE Task → analysisId → Quality Gate)

SonarCloud evaluation is asynchronous:
1) Scanner uploads analysis payload to SonarCloud
2) SonarCloud creates a CE task (queued/running)
3) CE task completes with SUCCESS, producing an analysisId
4) Quality Gate is evaluated against that analysisId
5) CI reads the Quality Gate status and enforces pass/fail

Therefore: a correct merge blocker must poll CE status until the analysisId exists, then query Quality Gate status using analysisId.

---

## Required Artifacts: report-task.txt

Most scanners emit report-task.txt, a key=value file that links the scanner run to the CE task.

Typical keys:
- ceTaskId
- ceTaskUrl
- serverUrl
- dashboardUrl

Common locations:
- .scannerwork/report-task.txt
- target/sonar/report-task.txt
- build/sonar/report-task.txt

In CI, the merge-gating step must run in the same workspace context (or receive report-task.txt as an artifact) so it can deterministically bind the Quality Gate query to the exact analysis produced by the scan.

---

## SonarCloud Web API Surfaces Used

Compute Engine task polling:
- GET /api/ce/task?id=<ceTaskId>
Returns:
- task.status (PENDING/RUNNING/SUCCESS/FAILED/CANCELED)
- task.analysisId (present when SUCCESS)

Quality Gate evaluation bound to analysis snapshot:
- GET /api/qualitygates/project_status?analysisId=<analysisId>
Returns:
- projectStatus.status (OK/ERROR/NONE depending on configuration)
- projectStatus.conditions (metric thresholds, actual values, comparators)

Fallback (less deterministic immediately after scan):
- GET /api/qualitygates/project_status?projectKey=<projectKey>&branch=<branch>
- GET /api/qualitygates/project_status?projectKey=<projectKey>&pullRequest=<prKey>

Hard recommendation: use analysisId for merge blocking.

---

## Authentication (SonarCloud Token Model)

SonarCloud uses token-based authentication commonly via HTTP Basic where:
- username = token
- password = empty

Header format:
- Authorization: Basic base64("<TOKEN>:")

Operational requirements:
- SONAR_TOKEN must be injected via CI secrets
- token must be scoped appropriately to read analysis and quality gate status
- token rotation and access reviews are mandatory in hardened environments

---

## Included Tooling

### zeid_data_sonar_merge_blocker.py

A SonarCloud-compatible merge gate enforcer that:
- Locates report-task.txt (or accepts explicit CE task inputs)
- Polls CE task until SUCCESS (or fails/timeout)
- Fetches Quality Gate status for the resulting analysisId
- Returns deterministic exit codes for CI enforcement

Exit codes (Zeid Data convention):
- 0: Quality Gate OK (allow merge)
- 1: Quality Gate ERROR (block merge)
- 2: Inconclusive/config/network failure (treat as hard fail for protected branches)

Rationale: An inconclusive gate is equivalent to “control bypass.” In protected workflows, non-determinism should block merges until proven otherwise.

---

## CI Configuration Surface (Environment Variables)

Recommended variables:
- SONAR_HOST_URL (or SONAR_URL): SonarCloud base URL (typically https://sonarcloud.io)
- SONAR_TOKEN: SonarCloud token (CI secret)
- SONAR_REPORT_TASK_FILE: Optional explicit path to report-task.txt
- SONAR_CE_TASK_ID / SONAR_CE_TASK_URL: Optional explicit CE identifiers
- SONAR_TIMEOUT_SECONDS: Max time to wait for CE completion (default commonly 300)
- SONAR_POLL_SECONDS: Poll interval (default commonly 5)

Fallback mode variables (only if analysisId is unavailable):
- SONAR_PROJECT_KEY
- SONAR_BRANCH
- SONAR_PULL_REQUEST

---

## Execution Pattern (Reference Workflow)

Required ordering:
1) Checkout
2) Build/test (optional but recommended before scan)
3) SonarCloud scan step
4) Merge gate enforcement (this directory’s tooling)
5) Artifact retention (optional but recommended)

Minimal enforcement step (CE + analysisId mode) after scan:
- Ensure report-task.txt exists
- Run the merge blocker with SONAR_HOST_URL and SONAR_TOKEN

If report-task.txt is not in the default locations:
- Set SONAR_REPORT_TASK_FILE explicitly

If your pipeline isolates workspaces between stages:
- Persist report-task.txt and scanner outputs as artifacts and restore them prior to the gating step.

---

## Evidence Output and Retention (Audit-Ready CI)

SonarCloud gating can be treated as an evidence-producing control. Recommended retained artifacts per pipeline run:
- scanner logs (raw)
- report-task.txt (raw)
- CE task JSON response (final)
- Quality Gate JSON response (final)
- commit SHA, branch, PR id, pipeline run id, timestamps
- derived summary line emitted by the gate tool

Optional hardening:
- compute a hash manifest over all evidence artifacts
- sign the manifest (CI key or KMS-backed signing)
- store artifacts immutably (WORM store or retention bucket)

This supports:
- change-control attestation
- post-incident audit reconstruction
- regression timeline for quality/security drift

---

## Failure Modes (SonarCloud Operational Notes)

CE polling timeouts:
- Causes: transient SonarCloud latency, organization-wide queue backlog, CI egress issues, scanner upload delays.
- Mitigation: increase SONAR_TIMEOUT_SECONDS, reduce concurrency, ensure stable egress/DNS, avoid overly aggressive polling.

Quality Gate mismatch or NONE:
- Causes: analysis not associated with correct branch/PR, wrong projectKey, gating called too early, scanner misconfigured.
- Mitigation: enforce analysisId binding, verify scanner flags for branch/PR, confirm project configuration in SonarCloud UI.

401/403 errors:
- Causes: invalid/revoked token, insufficient access to the project/org.
- Mitigation: rotate token, validate org permissions, reduce token scope only after confirming minimum required privileges.

Pipeline flakiness:
- Causes: shared runners, intermittent networking, rate limiting.
- Mitigation: retry only on network-class failures (not on deterministic ERROR gates), keep polling conservative, use stable runners for protected branches.

---

## Policy Engineering (Quality Gate Design)

For SonarCloud, Quality Gates should be treated as enforced policy artifacts. Strong defaults:
- Fail on any new vulnerability on new code
- Require new code coverage thresholds aligned to risk tier
- Require security hotspots reviewed on new code
- Control duplication and maintainability ratios on new code

Avoid policy drift:
- document gate thresholds and change control process
- standardize gates across repos where possible
- require explicit approvals for exceptions

---

## Maintainers

Zeid Data Research Labs
Security Engineering / SDLC Controls
