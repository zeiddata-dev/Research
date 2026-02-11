# Zeid Data — Sonar Content (Static Analysis, Quality Gates, CI Enforcement) 🧪🔒

# Fixed what Sonar flagged. If it finds more, I’m assuming it’s just lonely. 🤖

Welcome to the part of the repo where we take static analysis output and turn it into deterministic, CI-enforced policy outcomes. ⚙️✅

Remember: nothing says “modern software engineering” like a pipeline that refuses to merge your PR until it has received the proper blessing from an asynchronous background job that may or may not be having a feelings-based relationship with your network today. 🙃⏳

And yes—this exists because someone looked at “Quality Gate: ERROR” and decided that was a personal attack. So now we have policy enforcement. You’re welcome. 😌🚧

## What This Directory Is For 🎯

Primary objectives:

* Enforce Sonar Quality Gates as merge blockers with explicit, machine-verifiable exit codes. 🛑
* Avoid race conditions by polling Sonar Compute Engine (CE) completion prior to reading the Quality Gate. ⏱️
* Support both SonarQube (self-hosted) and SonarCloud (hosted) by using the Sonar Web API as the single integration surface. ☁️
* Produce operationally useful, automation-friendly output for pipelines and evidence retention. 🧾

Translation: stop “it passed on my machine” and start “it passed in CI, on record, with timestamps.” 😤

---

## Analysis Lifecycle Model (Compute Engine → analysisId → Quality Gate) 🔄

Sonar analysis is asynchronous, because of course it is. Uploading analysis data does not mean analysis is complete, and it definitely does not mean Quality Gate evaluation is ready. The correct lifecycle is: 🤷‍♂️

1. Scanner uploads analysis payload 📤
2. Sonar enqueues a Compute Engine task (CE task)
3. CE task transitions through statuses (PENDING/RUNNING) to SUCCESS (or FAILED/CANCELED, if it’s choosing violence) 💥
4. Upon SUCCESS, Sonar emits an analysisId representing that specific analysis snapshot 🆔
5. Quality Gate is evaluated against that analysisId 🚦
6. A merge-blocking step fetches Quality Gate state for that exact analysisId and fails the pipeline if status != OK 🚫

Implication: a robust merge blocker binds Quality Gate evaluation to analysisId derived from CE completion, not to vague “project status” queries that can drift across branches, time, and reality. 🌀

---

## Canonical Scanner Artifact: report-task.txt 📄

Most Sonar scanners emit a key=value file commonly named report-task.txt. It contains identifiers needed to locate the CE task and the analyzed project context. Typical keys include:

* ceTaskId
* ceTaskUrl
* serverUrl
* dashboardUrl

Common locations (scanner/build dependent):

* .scannerwork/report-task.txt (sonar-scanner default)
* target/sonar/report-task.txt (common for Maven sonar:sonar)
* build/sonar/report-task.txt (varies; often Gradle-related layouts)

Best practice: treat report-task.txt as the authoritative linkage between the scanner invocation and the resulting CE task + analysisId. In CI, keep it available to the merge-blocking step (same workspace, artifact passing, or explicit path configuration). 📁

In other words: don’t delete the breadcrumb trail and then act surprised when you’re lost. 😑🗺️

---

## Sonar Web API Surfaces Used for Merge Blocking 🌐

Compute Engine task polling (binds to a specific analysis execution):

* GET /api/ce/task?id=<ceTaskId>
  Returns: task.status and task.analysisId once complete.

Quality Gate evaluation (binds to a specific analysis snapshot):

* GET /api/qualitygates/project_status?analysisId=<analysisId>
  Returns: projectStatus.status and projectStatus.conditions.

Fallback evaluation (less reliable immediately after scan; depends on correct branch/PR correlation and timing):

* GET /api/qualitygates/project_status?projectKey=<projectKey>&branch=<branch>
* GET /api/qualitygates/project_status?projectKey=<projectKey>&pullRequest=<prKey>

Strong recommendation: prefer analysisId mode whenever possible for deterministic merge blocking. If you enjoy nondeterminism, there are plenty of other places to find it (like distributed systems, elections, and printer drivers). 😅

---

## Included Tooling 🧰

### zeid_data_sonar_merge_blocker.py

Purpose: fail a pipeline when the Sonar Quality Gate fails by performing:

* Task discovery (via report-task.txt or explicit ceTaskId/ceTaskUrl)
* CE polling until analysis completion (or timeout/failure)
* Quality Gate fetch for the resulting analysisId
* Exit code mapping for CI merge blocking

Typical exit code contract (recommended):

* 0: Quality Gate OK (merge allowed) ✅
* 1: Quality Gate ERROR (merge blocked) ❌
* 2: Inconclusive/config/network error (treat as hard failure in protected branches) ⚠️

Operational note: exit code 2 should be treated as a serious pipeline health issue. If a branch is protected, an inconclusive gate should not allow merges because it bypasses the intended control. Yes, this means “the internet was flaky” is no longer an acceptable risk strategy. 📶🚫

---

## Authentication (Token-as-Username Basic Auth) 🔐

Sonar Web API commonly authenticates via HTTP Basic Authorization where the token is the username and the password is empty:

* Authorization: Basic base64("<TOKEN>:")

Security guidance:

* Store SONAR_TOKEN in CI secret storage. 🔒
* Use least privilege tokens.
* Rotate tokens on a schedule; disable tokens on IR triggers. 🔁
* Never print tokens to logs. 🚫

Also: if you print tokens to logs, you didn’t “make a mistake,” you created a free community credential distribution program. 🤦‍♂️

---

## Configuration Surface (Environment Variables and CLI) ⚙️

Recommended CI variables:

* SONAR_HOST_URL or SONAR_URL: base Sonar URL
* SONAR_TOKEN: API token used for CE polling and Quality Gate retrieval
* SONAR_REPORT_TASK_FILE: explicit path to report-task.txt
* SONAR_CE_TASK_ID / SONAR_CE_TASK_URL: explicit CE task identifiers if report-task.txt is unavailable
* SONAR_PROJECT_KEY: project key for fallback mode when analysisId is unavailable
* SONAR_BRANCH: branch name for fallback mode
* SONAR_PULL_REQUEST: PR identifier for fallback mode
* SONAR_TIMEOUT_SECONDS: CE polling maximum wall time (default typically 300)
* SONAR_POLL_SECONDS: CE polling interval (default typically 5)

CLI flags generally mirror variables for deterministic execution in mixed CI environments. ✅

---

## Usage Patterns 🧭

Preferred (CE polling + analysisId binding):

* Run scanner
* Ensure report-task.txt exists in workspace
* Run merge blocker with SONAR_HOST_URL and SONAR_TOKEN

Explicit task file path:

* Use SONAR_REPORT_TASK_FILE or --report-task-file

Explicit CE task:

* Use SONAR_CE_TASK_URL or --ce-task-url

Fallback mode (projectKey + branch/PR):

* Use SONAR_PROJECT_KEY and optionally SONAR_BRANCH or SONAR_PULL_REQUEST
* Use only when CE linkage is impossible; understand it may be nondeterministic right after scans 🎲

---

## Output Semantics (CI-Friendly) 🧾

Expected output should be single-line, log-parseable summaries plus optional JSON for evidence/debugging:

* Quality Gate=OK.
* Quality Gate=ERROR. Failed conditions: <metric/comparator/threshold/actual> ...

Optional JSON mode should print the CE payload and Quality Gate payload for:

* audit evidence of gate outcome
* regression investigation
* governance reporting

Evidence retention pattern:

* Store scanner logs, report-task.txt, CE response JSON, Quality Gate response JSON, commit SHA, branch/PR metadata, pipeline run ID, and timestamps. ⏰
* Hash and sign artifact bundles if required. 🔏

Because “trust me” isn’t an artifact, and it doesn’t satisfy auditors—or your future self at 2:13 AM. 🕑

---

## Failure Modes and Deep Diagnostics 🔬

CE task never reaches SUCCESS: causes include backlog, misconfigured workers, analyzer errors, upload failures, permissions, or network/proxy faults. Mitigation: increase SONAR_TIMEOUT_SECONDS, inspect /api/ce/task for errors, validate server health, verify plugin compatibility, and ensure scanner configuration is correct.

Quality Gate fetch is inconclusive/unknown: causes include CE not complete, wrong base URL, mismatched serverUrl, missing branch/PR metadata, or branch attribution issues. Mitigation: prefer analysisId mode, normalize base URL usage, ensure scanner passes correct branch/PR parameters, and don’t query before CE completion.

Authentication errors (401/403): causes include invalid/revoked token or insufficient permissions. Mitigation: rotate token, verify access rights, confirm project visibility and org permissions.

Pipeline flakiness: causes include shared runners, intermittent egress, DNS instability, rate limiting, and API latency. Mitigation: retry transient failures, keep polling intervals conservative, and centralize network policy enforcement.

---

## Quality Gate Policy Engineering (Zeid Data Perspective) 🧠

Treat Quality Gates as versioned policy artifacts. Define gates explicitly for new code vs overall code and align thresholds to release readiness and SDLC controls. Common critical dimensions include:

* New vulnerabilities and hotspot review status
* Coverage on new code and test completeness
* Duplications and maintainability ratio/technical debt
* Reliability and bug density on changed components

Avoid policy drift:

* Enforce consistent gates across repos via central governance and documented overrides.
* Require explicit change control for threshold updates.
* Consider signing/attesting policy baselines in regulated environments. 🔏

---

## Roadmap Extensions (Optional Enhancements) 🚀

Potential additions:

* Policy-as-code mappings and gate configuration manifests
* Evidence bundle generator with hash manifests + signature support
* PR comment automation summarizing failed conditions and deltas
* Monorepo aggregation patterns and per-module gates
* Baseline onboarding workflows for legacy code and “new code” focus migration

---

## Maintainers

Zeid Data Research Labs
Security Engineering / SDLC Controls
