# Zeid Data — Data Recovery Tools

**Authorized use only. Do not use on systems or data you do not own or have explicit permission to analyze.**

This directory is a **flat** collection of Zeid Data utilities and training assets related to **data recovery workflows** and **digital forensics readiness**. The focus is evidence-first operations: integrity checks, repeatable handling, and audit-ready outputs.

## What this repo is for
- DFIR workflow enablement (case scaffolding, evidence intake patterns, manifests)
- Integrity verification and reporting (hash checks, chain-of-custody logs)
- Training labs and simulations (safe datasets, simulated deletion/restore inside containers)
- IR readiness utilities and templates (SOPs, runbooks, reporting packs)

## What this repo is NOT for
To keep usage ethical and safe, Zeid Data does not publish tooling here that:
- recovers deleted data from real disks
- reads raw block devices (e.g., `/dev/*`, `PhysicalDrive*`, `disk0`)
- performs file carving, undelete algorithms, or filesystem parsing (NTFS/EXT/APFS)
- includes instructions intended to bypass access controls or recover data without authorization

If you need real-world recovery for **your own** data, use approved commercial tools or consult a qualified DFIR provider.

## Flat folder layout (this directory)
All items live at the same level. Typical files you may see here:

- `DRT_WORKFLOW_TRAINER/`  
  Safe training simulator for evidence workflows using synthetic data and simulated deletion (no raw disk ops).

- `HASH_MANIFEST_UTIL/`  
  Hashing + manifest generation (JSON/CSV), verification helpers, and integrity checks.

- `CHAIN_OF_CUSTODY_LOGGER/`  
  Append-only custody logging utilities (tamper-evident / hash-chained).

- `REPORT_PACK_BUILDER/`  
  Generates human-readable report packs (Markdown, optional PDF).

- `SYNTHETIC_DATASETS/`  
  Synthetic training datasets only (no real customer data).

- `TEMPLATES/`  
  Chain-of-custody templates, evidence intake forms, SOP starters.

> Each folder is self-contained and should include its own `README.md` explaining purpose and usage.

## Required safety guardrails for every tool in this directory
- Operate only on **user-provided folders** and/or **tool-generated containers**
- Never operate on raw disks or device paths
- Never write into evidence inputs; always output to a separate folder
- Produce SHA-256 (or stronger) hashes and store them in a manifest
- Log actions with timestamps and parameters (audit-friendly)
- Include an explicit scope statement in each tool’s README

## Contributing (internal)
When adding a new tool folder:
1. Include `README.md` + `SECURITY.md` that clearly states non-goals and guardrails
2. Add `tests/` for hashing, manifest generation, and logging correctness
3. Keep it offline-ready (no external services required)
4. Avoid adding capabilities that could be repurposed for unauthorized access

## Support
Open an issue or PR with:
- tool name + version
- OS + Python version
- expected vs actual behavior
- sanitized logs (no sensitive data)

---

**Zeid Data principle:** If it didn’t generate evidence, it didn’t happen.
```
