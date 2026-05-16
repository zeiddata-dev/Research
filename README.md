<p align="center">
  <img src="./assets/images/zd_banner_3.png" alt="Zeid Data Research Lab" width="100%">
</p>

<h1 align="center">Zeid Data Research</h1>

<p align="center">
  Security research, detection engineering, data tooling, automation, and experiments.
  <br>
  Built for receipts, not vibes. The robot is friendly. The pipeline is not.
</p>

<p align="center">
  <a href="./projects">Projects</a> ·
  <a href="./detections">Detections</a> ·
  <a href="./malware">Malware Research</a> ·
  <a href="./scripts">Scripts</a> ·
  <a href="./docs">Docs</a> ·
  <a href="./workbooks">Workbooks</a> ·
  <a href="./SECURITY.md">Security</a>
</p>

<p align="center">
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge">
  <img alt="Research Lab" src="https://img.shields.io/badge/research-lab-38bdf8?style=for-the-badge">
  <img alt="Security Tools" src="https://img.shields.io/badge/security-tools-f97316?style=for-the-badge">
  <img alt="Evidence First" src="https://img.shields.io/badge/evidence-first-a855f7?style=for-the-badge">
</p>

---

## What this repo is

This is the public Zeid Data research lab for security-focused software, analytics workflows, detection engineering, malware research notes, automation scripts, templates, white papers, and workbook artifacts.

The operating model is simple:

```text
collect -> normalize -> analyze -> validate -> document -> ship with receipts
```

If a tool cannot explain what it read, what it changed, and what evidence supports the output, it gets escorted back to the lab bench by a disappointed robot.

## Lab map

| Area | What it is for | Link |
|---|---|---|
| Projects | Broader software and research projects | [`projects/`](./projects) |
| Security detections | Rules, detection engineering content, and defensive analytics | [`detections/`](./detections) |
| Malware research | Malware analysis and defensive research material | [`research/malware/`](./malware) |
| Scripts | Automation, validators, collectors, helpers, and repeatable tooling | [`tools/scripts/`](./scripts) |
| Documentation | Design notes, references, constraints, and operating guidance | [`docs/`](./docs) |
| Templates | Reusable report, workflow, and documentation templates | [`templates/`](./templates) |
| White papers | Longer-form research and technical writing | [`research/research/white-papers/`](./white_papers) |
| Workbooks | Dashboard or workbook-style artifacts | [`workbooks/`](./workbooks) |
| Media | Repo-local visual assets and banners | [`assets/images/`](./media) |
| Content | Public-facing content and supporting material | [`content/`](./content) |

## Featured operating principles

<details open>
<summary><strong>Evidence first</strong></summary>

Outputs should be traceable to inputs. Prefer structured results, stable schemas, reproducible runs, and documented assumptions over hand-wavy "seems fine" engineering.
</details>

<details>
<summary><strong>Defensive and authorized</strong></summary>

Security material in this repository is intended for authorized research, defensive testing, privacy review, detection engineering, and audit workflows. It is not a guide for credential theft, unauthorized access, stealth, evasion, abuse, or bypassing protections.
</details>

<details>
<summary><strong>Automation with guardrails</strong></summary>

Scripts should be non-interactive where possible, explicit about inputs and outputs, safe to run in controlled environments, and clear about failure modes. If a command can break something, it should say what it touches before it touches it.
</details>

<details>
<summary><strong>Robot humor, human accountability</strong></summary>

The lab voice can be weird. The engineering cannot be. Jokes are allowed. Fake claims are not.
</details>

## How to use this repo

Start by inspecting the area that matches your goal.

```bash
git clone https://github.com/zeiddata-dev/Research.git
cd Research

find . -maxdepth 2 -name README.md -print | sort
find . -maxdepth 2 -type f \( -name 'requirements*.txt' -o -name 'pyproject.toml' -o -name 'package.json' -o -name 'Makefile' \) -print | sort
```

Then read the module-level documentation before running tools. Different folders may have different requirements, assumptions, and safety boundaries.

## Quality bar

Good additions should include:

- A clear purpose.
- Safe default behavior.
- Public-safe documentation.
- Reproducible commands or tests where applicable.
- Machine-readable output when the artifact is meant for automation.
- Explicit assumptions and limits.
- No secrets, tokens, private URLs, private logs, or personal data.

## Security and responsible disclosure

Do not open public issues for sensitive vulnerabilities. Use the repository security policy for reporting guidance: [`SECURITY.md`](./SECURITY.md).

Security research in this repo should remain authorized, defensive, and privacy-preserving. The lab does not need surprise crimes in the test suite.

## GitHub profile draft

This repository is not the special `.github` profile repository, so the reusable profile README draft lives here:

[`docs/guides/profile-readme.md`](./docs/guides/profile-readme.md)

Copy that file into `.github/profile/README.md` in the Zeid Data GitHub profile repository when ready.

## Maintainer notes

- Keep links real.
- Keep examples sanitized.
- Keep claims tied to repo contents.
- Keep generated assets local when practical.
- Keep the robot jokes, but do not let them drive architecture.

## License

This repository uses the MIT License unless a subfolder states otherwise. See [`LICENSE.md`](./LICENSE.md).
