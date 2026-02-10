# Zeid Data — Sonar Content (Static Analysis, Quality Gates, CI Enforcement)

This directory contains Zeid Data SonarQube/SonarCloud integration assets intended to convert static analysis output into deterministic, CI-enforced policy outcomes. The emphasis is on merge-blocking Quality Gate evaluation, strict reproducibility, and evidence-grade output suitable for SDLC control frameworks. The content here assumes you already execute a Sonar scanner (language/build-tool specific) and need to enforce the Quality Gate decision as a hard pipeline barrier across CI systems (GitHub Actions, GitLab CI, Jenkins, Azure DevOps, etc.).

---

## What This Directory Is For

Primary objectives:
- Enforce Sonar Quality Gates as merge blockers with explicit, machine-verifiable exit codes.
- Avoid race conditions by polling Sonar Compute Engine (CE) completion prior to reading the Quality Gate.
- Support both SonarQube (self-hosted) and SonarCloud (hosted) by using the Sonar Web API as the single integration surface.
- Produce operationally useful, automation-friendly output for pipelines and evidence retention.

---

## Analysis Lifecycle Model (Compute Engine → analysisId → Quality Gate)

Sonar analysis is asynchronous. A scanner step uploading analysis data does not imply analysis completion or Quality Gate evaluation is ready. The correct lifecycle is:

1) Scanner uploads analysis payload
2) Sonar enqueues a Compute Engine task (CE task)
3) CE task transitions through statuses (PENDING/RUNNING) to SUCCESS (or FAILED/CANCELED)
4) Upon SUCCESS, Sonar emits an analysisId representing that specific analysis snapshot
5) Quality Gate is evaluated against that analysisId
6) A merge-blocking step should fetch Quality Gate state for the exact analysisId and fail the pipeline if status != OK

Implication: A robust merge blocker must bind Quality Gate evaluation to analysisId derived from CE completion, not to broad project queries that can drift across branches or time.

---

## Canonical Scanner Artifact: report-task.txt

Most Sonar scanners emit a key=value file commonly named report-task.txt. It contains identifiers needed to locate the CE task and the analyzed project context. Typical keys include:
- ceTaskId
- ceTaskUrl
- serverUrl
- dashboardUrl

Common locations (scanner/build dependent):
- .scannerwork/report-task.txt (sonar-scanner default)
- target/sonar/report-task.txt (common for Maven sonar:sonar)
- build/sonar/report-task.txt (varies; often Gradle-related layouts)

Best practice: Treat report-task.txt as the authoritative linkage between the scanner invocation and the resulting CE task and analysisId. In CI, ensure it remains available to the merge-blocking step (same workspace, artifact passing, or explicit path configuration).

---

## Sonar Web API Surfaces Used for Merge Blocking

Compute Engine task polling (binds to a specific analysis execution):
- GET /api/ce/task?id=<ceTaskId>
Returns: task.status and task.analysisId once complete.

Quality Gate evaluation (binds to a specific analysis snapshot):
- GET /api/qualitygates/project_status?analysisId=<analysisId>
Returns: projectStatus.status and projectStatus.conditions.

Fallback evaluation (less reliable immediately after scan; depends on correct branch/PR correlation and timing):
- GET /api/qualitygates/project_status?projectKey=<projectKey>&branch=<branch>
- GET /api/qualitygates/project_status?projectKey=<projectKey>&pullRequest=<prKey>

Strong recommendation: Prefer analysisId mode whenever possible for deterministic merge blocking.

---

## Included Tooling

### zeid_data_sonar_merge_blocker.py

Purpose: Fail a pipeline when the Sonar Quality Gate fails by performing:
- Task discovery (via report-task.txt or explicit ceTaskId/ceTaskUrl)
- CE polling until analysis completion (or timeout/failure)
- Quality Gate fetch for the resulting analysisId
- Exit code mapping for CI merge blocking

Typical exit code contract (recommended):
- 0: Quality Gate OK (merge allowed)
- 1: Quality Gate ERROR (merge blocked)
- 2: Inconclusive/config/network error (treat as hard failure in protected branches)

Operational note: Exit code 2 should be treated as a serious pipeline health issue; if a branch is protected, an inconclusive gate should not allow merges because it bypasses the intended control.

---

## Authentication (Token-as-Username Basic Auth)

Sonar Web API commonly authenticates via HTTP Basic Authorization where the token is the username and the password is empty. The header format is:
- Authorization: Basic base64("<TOKEN>:")

Security guidance:
- Store SONAR_TOKEN in CI secret storage (GitHub Secrets, GitLab Variables, Vault, etc.).
- Use least privilege tokens with the minimum scope required to read CE task status and Quality Gate status for the project.
- Rotate tokens on a schedule; disable tokens on incident response triggers.
- Never print tokens to logs; disable verbose debug output in shared runners.

---

## Configuration Surface (Environment Variables and CLI)

Recommended CI variables:
- SONAR_HOST_URL or SONAR_URL: Base Sonar URL, e.g. https://sonarcloud.io or https://sonar.internal.example
- SONAR_TOKEN: API token used for CE polling and Quality Gate retrieval
- SONAR_REPORT_TASK_FILE: Explicit path to report-task.txt if not in standard locations
- SONAR_CE_TASK_ID / SONAR_CE_TASK_URL: Explicit CE task identifiers if report-task.txt is unavailable
- SONAR_PROJECT_KEY: Project key for fallback mode when analysisId is unavailable
- SONAR_BRANCH: Branch name for fallback mode
- SONAR_PULL_REQUEST: PR identifier for fallback mode
- SONAR_TIMEOUT_SECONDS: CE polling maximum wall time (default typically 300)
- SONAR_POLL_SECONDS: CE polling interval (default typically 5)

CLI flags generally mirror the variables for deterministic execution in mixed CI environments.

---

## Usage Patterns

Preferred (CE polling + analysisId binding):
- Run scanner
- Ensure report-task.txt exists in workspace
- Run merge blocker with SONAR_HOST_URL and SONAR_TOKEN

Explicit task file path:
- Use SONAR_REPORT_TASK_FILE or --report-task-file to point directly to report-task.txt

Explicit CE task:
- Use SONAR_CE_TASK_URL or --ce-task-url when the CE task linkage is known by the pipeline system and the report-task.txt is not available

Fallback mode (projectKey + branch/PR):
- Use SONAR_PROJECT_KEY and optionally SONAR_BRANCH or SONAR_PULL_REQUEST
- Use only when CE linkage is impossible; understand it may be nondeterministic in immediate post-scan windows

---

## Output Semantics (CI-Friendly)

Expected output should be single-line, log-parseable summaries plus optional JSON for evidence/debugging:
- Quality Gate=OK.
- Quality Gate=ERROR. Failed conditions: <metric/comparator/threshold/actual> ...

Optional JSON mode should print the CE payload and Quality Gate payload. This can be captured as build artifacts for:
- audit evidence of gate outcome
- regression investigation
- governance reporting (time series of failing conditions)

Evidence retention pattern:
- Store scanner logs, report-task.txt, CE response JSON, Quality Gate response JSON, commit SHA, branch/PR metadata, pipeline run ID, and timestamps.
- Hash and sign artifact bundles if required by your SDLC attestation controls.

---

## Failure Modes and Deep Diagnostics

1) CE task never reaches SUCCESS:
- CE worker backlog, misconfigured compute workers, plugin/analyzer errors, analysis upload failures, insufficient permissions, or network/proxy faults.
Mitigation:
- Increase SONAR_TIMEOUT_SECONDS, inspect /api/ce/task payload for errorMessage, validate server health and background tasks, verify plugin compatibility and analyzer presence, and ensure scanner is configured with correct source/binary paths.

2) Quality Gate fetch is inconclusive/unknown:
- CE not complete, wrong sonar-url base, mismatched serverUrl vs configured base URL, fallback mode missing branch/PR metadata, or branch analysis not correctly attributed by scanner flags.
Mitigation:
- Prefer analysisId mode, normalize base URL usage, ensure scanner passes correct branch/PR parameters, and avoid calling Quality Gate endpoints before CE completion.

3) Authentication errors (401/403):
- Invalid token, revoked token, wrong token type, or insufficient project permissions.
Mitigation:
- Rotate token, verify access rights, ensure project visibility, confirm token scopes and organization permissions.

4) Pipeline flakiness:
- Shared runners with intermittent egress, DNS instability, rate limiting, or transient Sonar API latency.
Mitigation:
- Add retry logic around transient failures (but not around deterministic ERROR gates), keep polling interval conservative, and centralize network policy enforcement.

---

## Quality Gate Policy Engineering (Zeid Data Perspective)

Treat Quality Gates as versioned policy artifacts. Define gates explicitly for new code vs overall code and align thresholds to release readiness and SDLC controls. Common critical dimensions include:
- New vulnerabilities and security hotspots review status
- Coverage on new code and test completeness
- Duplications and maintainability ratio/technical debt
- Reliability and bug density on changed components

Avoid policy drift:
- Enforce consistent gates across repos via central governance and documented overrides.
- Require explicit change control for gate threshold changes.
- Consider signing or attesting policy baselines in regulated environments.

---

## Roadmap Extensions (Optional Enhancements)

Potential additions to this directory include:
- Policy-as-code mappings and gate configuration manifests
- Evidence bundle generator with hash manifests and signature support
- PR comment automation that summarizes failed conditions and deltas
- Monorepo aggregation patterns and per-module gates
- Baseline onboarding workflows for legacy code and “new code” focus migration

---

## Maintainers

Zeid Data Research Labs
Security Engineering / SDLC Controls
