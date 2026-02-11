# SonarQube (Zeid Data)

Welcome to the **SonarQube** corner of the Zeid Data GitHub — where code gets interrogated, rated, and occasionally roasted with receipts.

If you’re here looking for vibes: this folder is for **static analysis**, **quality gates**, **security hotspots**, **issue evidence**, and **repeatable CI outputs** that can survive auditors, incident retros, and that one teammate who “doesn’t trust dashboards.”

> Wish I could code-check my own operating system. Unfortunately SonarQube doesn’t support scanning the human kernel yet.  
> (If it did, my `sleep()` function would fail Quality Gate daily, and my exception handling is… aspirational.)

---

## What This Repo Section Is For

- **SonarQube / SonarCloud patterns**: config, conventions, and CI wiring that works in real life (not just in blog posts written by people with unlimited time)
- **Quality Gate enforcement**: policy-as-code and “no, you can’t merge that” automation
- **Issue + Hotspot exports**: CSV/JSON artifacts you can hand to security/compliance without having to interpret dashboards like tea leaves
- **Evidence Packs**: deterministic bundles suitable for audits, incident reviews, and “prove it” conversations
- **Operational docs**: tuning, performance, analyzer quirks, and version drift survival strategies

---

## What SonarQube Actually Does (In Technical Terms, Not Marketing Terms)

SonarQube performs static analysis and computes measures across:
- **Reliability**: `bugs`, `reliability_rating`
- **Security**: `vulnerabilities`, `security_rating`
- **Security Hotspots**: code paths that require human review and threat context (aka “this might be fine, or it might be the beginning of a very long week”)
- **Maintainability**: `code_smells`, `sqale_rating`, `sqale_index`
- **Code Health**: `coverage`, `duplicated_lines_density`, `ncloc`

Zeid Data treats Sonar output as **evidence**, not vibes:
- *what* was scanned
- *when* it was scanned
- *which branch/PR* the data belongs to
- *what changed* (especially on “New Code”)
- *what policy blocked it* (Quality Gate conditions)

---

## Recommended Layout

```text
sonarqube/
  README.md
  docs/
    quality-gates.md
    metrics-and-thresholds.md
    pr-analysis.md
    evidence-and-audit.md
    troubleshooting.md
  tooling/
    zeid_data_sonar_evidence_pack.py
  ci/
    github-actions/
      sonar.yml
    gitlab/
      sonar.yml
    jenkins/
      Jenkinsfile.example
  examples/
    sonar-project.properties
    sonar-scanner.properties
    quality-gate.json (optional export)
```

---

## Quickstart

### 1) Minimal `sonar-project.properties`

Drop in repo root (or generate during CI):

```properties
sonar.projectKey=YOUR_PROJECT_KEY
sonar.projectName=YOUR_PROJECT_NAME
sonar.sources=.
sonar.sourceEncoding=UTF-8

# Strongly recommended exclusions
sonar.exclusions=**/node_modules/**,**/dist/**,**/build/**,**/.venv/**,**/vendor/**,**/coverage/**

# Optional (language/tooling dependent)
sonar.tests=.
sonar.test.inclusions=**/*test*,**/*spec*
```

### 2) Run `sonar-scanner`

```bash
sonar-scanner \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.login="$SONAR_TOKEN" \
  -Dsonar.projectKey="YOUR_PROJECT_KEY"
```

Pro tip: keep tokens in CI secrets. If you paste secrets into shell history, SonarQube can’t scan *that* regret.

---

## CI/CD Integration (Opinionated + Practical)

### Branch Analysis vs PR Analysis

- **Default branch (main/master)**: establishes baseline, trends, and long-term measures
- **PR analysis**: focuses on “New Code” and prevents regressions before merge

Common strategy:
- Gate PRs on **New Code** only (so legacy debt doesn’t brick forward progress)
- Enforce immediate failure on:
  - new critical vulnerabilities
  - dropped coverage on new code
  - new critical reliability issues

Because nothing says “engineering maturity” like blocking a merge that introduces a vulnerability with a commit message that says `minor cleanup`.

---

## Quality Gates (Policy-as-Code, With Teeth)

A Quality Gate is a set of conditions evaluated on the latest analysis context:
- project-wide
- per branch
- per pull request (preferred)

Typical conditions:
- **Security Rating on New Code** must be A
- **Reliability Rating on New Code** must be A
- **Coverage on New Code** >= threshold
- **No new critical vulnerabilities**
- **No new blocker issues**

Reality check:
- If your gate is too strict, teams will route around it.
- If your gate is too loose, it becomes a decorative sign that says “Please be safe.”

We aim for gates that:
- block truly risky changes
- keep PR feedback fast
- minimize “false-negative safety theater”

---

## Evidence Packs (Because “Trust Me Bro” Isn’t Audit-Ready)

This repo may include tooling that exports a **Sonar evidence bundle** from APIs into a portable pack:

Artifacts typically include:
- `meta.json` (context: sonar URL, project key, branch/PR, timestamps, filters)
- `evidence.json` (compiled measures + top issues/hotspots)
- `issues.csv` / `hotspots.csv` (portable exports)
- `summary.md` (human readable)
- optional `summary.pdf` (for people who still live in email attachments)

Example run:

```bash
python3 tooling/zeid_data_sonar_evidence_pack.py \
  --sonar-url "$SONAR_HOST_URL" \
  --token "$SONAR_TOKEN" \
  --project-key "YOUR_PROJECT_KEY" \
  --branch "main" \
  --top-issues 100 \
  --top-hotspots 100 \
  --raw \
  --pdf
```

This is where the code speaks for itself. Unlike me, when asked “how are you doing?” in a standup while my brain is running at 99% CPU.

---

## Sonar APIs (For People Who Read the Manual on Purpose)

Useful endpoints (exact shapes vary by SonarQube version and SonarCloud):
- `/api/measures/component` — measures & ratings (overall + “New Code” periods)
- `/api/issues/search` — issues with filters (severity/type/status)
- `/api/hotspots/search` — security hotspots
- `/api/qualitygates/project_status` — quality gate status for project/branch/PR

Important implementation notes:
- Field names and models shift between versions
- Some filters get deprecated (and still “work” until they don’t)
- Hotspot payloads are especially variable by plan/version

Translation: your integration should be **defensive**, not emotionally attached to perfect JSON.

---

## Operational Guidance

### Performance & Scale
- Large monorepos: tune exclusions aggressively and consider per-module analysis
- Keep CI logs: analysis failures are often config/environmental, not “Sonar being weird” (okay sometimes it is, but still)
- Avoid scanning generated code unless you enjoy false positives as a lifestyle

### What Metrics Usually Matter
- `vulnerabilities`, `security_hotspots`, `security_rating`
- `bugs`, `reliability_rating`
- `coverage`, `duplicated_lines_density`
- `sqale_rating`, `code_smells`

### What Sonar Is Not
- Not a pentest
- Not runtime protection
- Not a firewall
- Not a magical force field
- It will not stop prod from combusting because someone hardcoded `ALLOW_ALL = true`
- It *will* loudly remind you that you hardcoded `ALLOW_ALL = true`, and then stare at you until you fix it

---

## Troubleshooting (Common Pain)

### “Analysis succeeded but metrics are empty”
- Confirm `sonar.sources` points to actual code
- Confirm exclusions aren’t excluding everything (yes, this happens)
- Verify analyzers exist for the language(s)
- Ensure CI workspace contains source (not just build artifacts)

### “PR analysis not linked / shows as branch”
- Verify PR parameters (provider integration + PR key/ID)
- Ensure the scanner is executed in PR context with correct env vars
- Check Sonar UI for the analysis context (PR vs branch)

### “Auth errors”
- Token invalid/expired/insufficient permissions
- Wrong `SONAR_HOST_URL` (people love mixing UI base URL vs reverse-proxy URL)
- Secret not available in PR builds (fork restrictions)

### “Quality gate passes but I still feel bad”
Same. I wish I could run static analysis on my own operating system too.  
If I could, it would probably flag:
- “Cognitive complexity: HIGH”
- “Sleep coverage: LOW”
- “Unhandled exceptions: MANY”
- “Deprecated coping mechanisms: TRUE”

---

## Contributing

PRs welcome if they:
- increase evidence quality and repeatability
- reduce ambiguity in CI wiring
- improve resilience across SonarQube/SonarCloud + version drift
- keep the tone: high signal, low nonsense

---

## License

Unless otherwise noted, this folder follows the root repository license.

---

## Final Note

SonarQube is a mirror.  
It doesn’t hate you. It just reports what you wrote — with timestamps.
