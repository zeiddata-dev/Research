# Repository Structure Review

## Current structure observed

The repository is already organized around usable security and engineering deliverables:

- `projects/` contains runnable tools and applications.
- `detections/` contains detection content and investigation packs.
- `content/` contains vendor-specific network security material.
- `malware/` contains malware-family research and related detection material.
- `white_papers/` contains longer-form written guidance.
- `workbooks/` contains dashboard and workbook artifacts.
- `templates/` contains packaged evidence and incident response templates.
- `scripts/` contains shared automation, inventory, detection, and weekly-report scripts.
- `docs/` contains repository-level documentation and standards.
- `media/` contains public images and brand assets.

This is a good public-lab shape, but the current taxonomy mixes audience, artifact type, and maturity level in a few places. The biggest design issue is that research-style content is split across `content/`, `malware/`, and `white_papers/`, while runnable code is split across `projects/` and `scripts/` without a single manifest or lifecycle model.

## Design goals

A better structure should make these questions obvious without tribal knowledge:

1. Is this item runnable code, deployable security content, research, or a reusable asset?
2. Who is the target operator: engineer, analyst, auditor, or public reader?
3. What is the maturity: incubating, beta, stable, archived?
4. What inputs, outputs, tests, and evidence exist?
5. Can an AI coding assistant find the correct files without reading the entire repo?

## Recommended top-level structure

Use the current folders where possible, but converge toward this layout:

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── index.md
│   └── standards/
├── projects/
│   └── <project-name>/
├── detections/
│   └── <pack-name>/
├── research/
│   ├── malware/
│   ├── cves/
│   ├── vendor-security/
│   └── white-papers/
├── templates/
│   └── <template-pack>/
├── workbooks/
│   └── <platform-or-domain>/
├── scripts/
│   ├── automation/
│   ├── detection/
│   ├── inventory/
│   └── reporting/
├── schemas/
│   └── <domain>/
├── examples/
│   └── <module-or-domain>/
├── tests/
│   └── <module-or-domain>/
└── media/
    ├── brand/
    ├── diagrams/
    └── social/
```

## Migration recommendation

Do not perform a big-bang move. Use a staged migration that preserves existing links.

### Phase 1: Document and freeze the target shape

- Keep the current folders working.
- Add this structure standard and link it from `docs/index.md`.
- Add or update `project.yaml` files for runnable modules.
- Require every new module to follow the target module layout.

### Phase 2: Normalize names and module metadata

- Rename future module folders to kebab-case.
- Keep existing `zeid_data_*` paths until a planned release can absorb the churn.
- Add `status`, `owner`, `entrypoints`, `inputs`, `outputs`, and `tests` metadata to each module.
- Add `README.md` sections for quickstart, evidence produced, and validation commands.

### Phase 3: Consolidate research content

Move research-style content into `research/` over time:

- `malware/` → `research/malware/`
- CVE analysis currently under `detections/cve-*` → `research/cves/<cve-id>/` when it is write-up-heavy
- `white_papers/` → `research/white-papers/`
- `content/` vendor guidance → `research/vendor-security/` unless it becomes a deployable template or detection pack

Detection rules, queries, YARA, Sigma, SPL, KQL, and deployable content should stay in `detections/`.

### Phase 4: Separate shared code from product code

- Keep full tools and apps in `projects/<name>/`.
- Keep repo-level utilities in `scripts/`.
- Move reusable Python packages into `libs/` only when more than one project imports them.
- Add root `tests/` only for shared scripts, cross-repo validation, or repository policy checks.
- Keep project-specific tests inside each project.

## Standard module layout

Each runnable project or deployable pack should use this baseline:

```text
<module>/
├── README.md
├── project.yaml
├── pyproject.toml        # if Python package or app
├── src/                  # product code
├── scripts/              # module-local helper commands
├── examples/             # safe sample inputs and configs
├── tests/                # unit, fixture, and regression tests
├── docs/                 # design notes and operator guidance
├── releases/             # release artifacts and checksums
└── SECURITY.md           # when module has distinct security notes
```

For non-code content packs, use this lighter layout:

```text
<pack>/
├── README.md
├── pack.yaml
├── rules/                # Sigma/YARA/SPL/KQL/etc.
├── examples/             # sanitized telemetry or screenshots
├── tests/                # validation fixtures or query tests
├── docs/                 # tuning and operational notes
└── releases/             # packaged exports and checksums
```

## AI-response and code-design implications

This structure is intentionally AI-friendly:

- `AGENTS.md` defines behavior and safety boundaries for coding agents.
- `project.yaml` or `pack.yaml` gives assistants a quick machine-readable map.
- `README.md` gives humans a quick path to run, validate, and operate the module.
- `examples/` and `tests/` let an assistant verify behavior without guessing.
- `schemas/` prevents ad-hoc field names and brittle parsing.
- `docs/standards/` keeps design rules stable instead of burying them in conversations.

## Suggested next smallest action

Add a lightweight inventory manifest that lists every top-level module, type, status, owner, entrypoint, and validation command. That manifest will make the repo easier for humans, CI, and AI assistants to navigate before any directories are physically moved.
