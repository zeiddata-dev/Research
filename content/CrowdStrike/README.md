# Zeid Data — CrowdStrike Content Library

A central repository for Zeid Data–authored content offerings built to extend, operationalize, and accelerate CrowdStrike deployments.

This repo is designed to be **modular**: each content pack ships with its own README and HOWTO so you can install, configure, and validate it independently.

---

## What’s in here

Depending on the pack, you may find:

- Detection & hunting content (queries, scheduled searches, filters, baselines)
- Dashboards / reporting artifacts (SOC, governance, audit evidence views)
- Parsing / normalization helpers (field mapping, naming conventions)
- Tuning guidance (noise reduction, allowlists, exceptions, suppression logic)
- Evidence outputs (audit-ready exports, change logs, validation steps)
- Reference configurations (recommended settings, policy patterns)

> Not every pack contains every artifact type. Check the pack-level README for specifics.

---

## Repository layout

A typical structure looks like:

```text
/
├─ packs/
│  ├─ <pack-name-1>/
│  │  ├─ README.md
│  │  ├─ HOWTO.md
│  │  ├─ content/
│  │  ├─ examples/
│  │  └─ validation/
│  └─ <pack-name-2>/
│     ├─ README.md
│     ├─ HOWTO.md
│     └─ ...
├─ docs/
│  ├─ glossary.md
│  ├─ conventions.md
│  └─ troubleshooting.md
├─ CHANGELOG.md
├─ LICENSE
└─ README.md
```

**packs/** is the source of truth. If you only read one thing per pack, read:
- `packs/<pack-name>/README.md` (what it is + what it includes)
- `packs/<pack-name>/HOWTO.md` (install/config/validate)

---

## Quick start

1. **Pick a pack** under `packs/`.
2. Read the pack’s **README** to confirm prerequisites and compatibility.
3. Follow the pack’s **HOWTO** for:
   - Deployment steps
   - Required permissions / roles
   - Configuration values
   - Validation / test steps
4. Use the pack’s **validation** artifacts to confirm it’s working as intended.
5. Tune using the pack’s recommended suppression/allowlist guidance (if provided).

---

## Compatibility & prerequisites

Each pack may target different CrowdStrike components and may have different requirements.

At minimum, expect:
- Access to the relevant CrowdStrike console features used by the pack
- Appropriate permissions to create/modify the required objects
- A test/validation window (recommended) before production rollout

See each pack README for exact requirements.

---

## How we version content

- This repository uses semantic versioning concepts at the **pack level**.
- Updates may include new content, tuning improvements, or breaking changes.
- Pack READMEs should state:
  - Pack version
  - Supported CrowdStrike components
  - Upgrade notes (when applicable)

See `CHANGELOG.md` for repo-level highlights.

---

## Contributing / requests

We welcome:
- Issue reports (false positives/negatives, parsing gaps, performance concerns)
- Feature requests (new coverage areas, dashboard views, evidence exports)
- Environment feedback (what worked, what didn’t, what required tuning)

When filing an issue, include:
- Pack name + version
- Environment notes (tenant size, relevant integrations)
- What you expected vs what happened
- Screenshots/redacted output if helpful

---

## Security & responsible use

These packs are intended for **defensive security operations** and governance monitoring.
Do not use this repository to facilitate unauthorized access or harmful activity.

---

## Licensing

See `LICENSE` for terms. Individual packs may include additional notices in their folders.

---

## About Zeid Data

Zeid Data builds practical security operations and governance content that emphasizes verifiable outcomes:

**“If it didn’t generate evidence, it didn’t happen.”**
