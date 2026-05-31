# Documentation Automation Plan

This repo will get better faster if the boring maintenance is automated. The goal is not to generate fake research. The goal is to keep indexes, stale-document reports, link checks, and weekly summaries current so humans can spend time on analysis.

## What should be automated

### 1. Weekly documentation inventory

Run once a week and produce a pull request with a generated inventory.

Recommended output:

- List every `README.md`, Markdown note, detection, script, workbook, and template.
- Flag missing folder-level `README.md` files.
- Flag docs without `last_reviewed` metadata.
- Flag broken relative links.
- Flag empty or placeholder sections.
- Produce `docs/generated/repo-inventory.md`.

Minimum safe implementation:

```text
find repo files -> classify by path -> parse markdown headings -> check relative links -> write inventory -> open PR
```

Do not let this job rewrite research claims or detection logic. Inventory only.

### 2. Monthly stale-doc report

Run monthly and open an issue or PR when docs are stale.

Suggested rules:

- `status: stable` docs should be reviewed at least every 180 days.
- `status: beta` docs should be reviewed at least every 90 days.
- `status: draft` docs should be reviewed at least every 45 days.
- Any doc without `last_reviewed` should be listed as `review_needed`.

Recommended output:

```markdown
# Stale Documentation Report

Generated: YYYY-MM-DD

| Path | Status | Last reviewed | Action |
|---|---|---|---|
| docs/example.md | draft | missing | add metadata and review |
```

### 3. Weekly research digest draft

Run weekly and create a draft Markdown file under `docs/generated/weekly-digests/`.

Digest inputs should be factual repo activity only:

- Recently changed files.
- New detections or scripts.
- New docs or templates.
- Open TODO markers.
- PRs merged that week.

Do not summarize external threat news unless a human adds a source and citation. The digest should not invent context.

### 4. README coverage checker

Run on pull requests.

Fail or warn when a new top-level module lacks:

- `README.md`
- Purpose section
- Usage or import steps, if applicable
- Evidence/output expectations
- Safety/scope notes for security content

### 5. Link and asset checker

Run on pull requests and weekly on `main`.

Check:

- Relative Markdown links.
- Local image paths.
- Badge URLs.
- Dead references to old paths such as `media/` when the public repo now uses `assets/`.

## Suggested GitHub Actions

Add these only when the repo is ready for automation PRs:

```text
.github/workflows/docs-inventory.yml
.github/workflows/docs-stale-report.yml
.github/workflows/readme-coverage.yml
.github/workflows/markdown-link-check.yml
```

## Suggested scripts

Keep scripts small and auditable:

```text
tools/scripts/docs/build_repo_inventory.py
tools/scripts/docs/check_markdown_links.py
tools/scripts/docs/check_readme_coverage.py
tools/scripts/docs/build_weekly_digest.py
```

Each script should emit machine-readable output:

```text
reports/docs-inventory.json
reports/docs-link-check.json
reports/docs-readme-coverage.json
```

Then generate human-readable Markdown from those JSON files. This keeps the evidence clean and the reports readable.

## Suggested auto-update workflow

A safe weekly flow:

1. GitHub Action runs on schedule.
2. Scripts generate JSON reports and Markdown summaries.
3. Action opens a PR named `docs: weekly documentation maintenance`.
4. Human reviews the PR.
5. Merge only if the generated report is accurate.

This avoids silent documentation drift and avoids letting automation publish unsupported claims.

## Rules for generated content

Generated docs may list, classify, count, and flag. They should not claim significance, risk, quality, or operational impact unless the evidence is present in the repo.

Allowed generated statements:

- `Path exists.`
- `README.md is missing.`
- `last_reviewed is older than 90 days.`
- `Relative link target not found.`
- `File changed in the last 7 days.`

Not allowed without human review:

- `This detection is high quality.`
- `This research is complete.`
- `This tool is production ready.`
- `This issue is critical.`

## Next implementation step

Start with the inventory job. It is the lowest-risk automation and gives the best map of what needs documentation work next.
