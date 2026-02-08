# SECURITY / SCOPE

**Authorized training use only. Do not use on systems or data you do not own or have explicit permission to analyze.**

## Scope
This project is a training simulator for DFIR evidence workflows:
- case setup and folder structure
- safe evidence intake (copying from an input folder)
- hashing and manifests
- append-only chain-of-custody logging (tamper-evident hash chain)
- synthetic training container generation
- simulated “deletion” and “restore” (metadata + container extraction)
- verification and reporting

## Non-goals (explicitly out of scope)
DRT will not:
- read raw block devices (e.g., `/dev/*`, `PhysicalDrive*`, `disk0`, etc.)
- implement file carving, undelete algorithms, or filesystem parsing (NTFS/EXT/APFS)
- provide instructions to recover real deleted data from real drives

## Guardrails
The CLI rejects suspicious paths that resemble raw-device targets.
All “restore” operations only extract from DRT-created synthetic containers into a case `working/` folder.
