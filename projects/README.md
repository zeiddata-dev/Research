<!-- ZEID DATA README HERO START -->
![Zeid Data projects banner](../assets/banners/readme/projects.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../tools/scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data Projects

This folder is for runnable tools, prototypes, applications, analyzers, collectors, validators, and repeatable workflows.

A project should be more than a pile of files. It should explain what it does, how to run it safely, what it outputs, and how to prove it worked.

## What belongs here

- CLI tools.
- Web apps or dashboards.
- Data pipelines.
- Evidence generators.
- Validators and auditors.
- Prototypes that may become standalone repositories later.

Small one-file helpers may belong in [`tools/scripts`](../tools/scripts) instead. If the artifact needs its own config, tests, examples, or release notes, it probably belongs here.

## Minimum project documentation

Each project should include:

| File | Purpose |
|---|---|
| `README.md` | Purpose, quickstart, inputs, outputs, validation, safety notes. |
| `project.yaml` | Lightweight metadata for indexing and automation. |
| `examples/` | Safe sample input or expected output, if practical. |
| `tests/` | Unit, smoke, or validation tests, if code is present. |
| `docs/` | Longer design notes or operating guidance, if needed. |

## Recommended `project.yaml`

```yaml
name: example-project
status: draft
owner: zeid-data
last_reviewed: 2026-05-31
tags: [security-research, evidence, automation]
entrypoints:
  - scripts/run-example.py
outputs:
  - reports/*.json
  - reports/*.md
public_safe: true
```

## Project README checklist

A useful project README should include:

- Purpose.
- Quickstart.
- Requirements.
- Configuration.
- Inputs and outputs.
- Validation commands.
- Failure modes.
- Safety and scope.
- Known limitations.
- License or repo license reference.

## Status model

Use one status consistently:

- `draft`: incomplete or early sketch.
- `incubating`: runnable experiment, changing often.
- `beta`: usable with documented limits.
- `stable`: reviewed and ready for reuse.
- `archived`: preserved, not maintained.

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`docs/automation.md`](../docs/automation.md)
