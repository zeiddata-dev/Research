# Zeid Data — Data Recovery Workflow Trainer (DRT)

**Authorized training use only. Do not use on systems or data you do not own or have explicit permission to analyze.**

This is an educational, offline-ready training tool that teaches **evidence handling** and **recovery workflow concepts**
using **synthetic data** and **simulated deletion**.

It **does not**:
- recover deleted files from real disks
- read raw block devices (e.g., `/dev/*`, `PhysicalDrive*`, `disk0`)
- perform file carving, undelete algorithms, or filesystem parsing (NTFS/EXT/APFS)

## Why this tool is safe
DRT only operates on:
1) a **user-provided folder of training files**, copied into a case's `evidence/` directory, and/or
2) a **synthetic training container** that DRT generates (a `.tar.gz` file with an internal manifest).

DRT never reads raw block devices and never implements real deletion recovery. “Deletion” is simulated by modifying
metadata in a manifest history and optionally extracting files from a synthetic container to a working directory.

## Requirements
- Python 3.11+
- No external services (offline).

Optional:
- PDF export: `reportlab` (if installed). Markdown reports always work.

## Install
This repo is pure Python. No install is required.

From the project root:

```bash
python -m zd_drt --help
```

## Quick start (60 seconds)
### 1) Initialize a case
```bash
python -m zd_drt init-case --cases-dir ./cases --case-id ZD-TRAIN-001 --analyst "Analyst Name" --auth "I am authorized to use this training dataset."
```

### 2) Ingest a training folder (safe copy + hashing + manifest)
```bash
python -m zd_drt ingest --cases-dir ./cases --case-id ZD-TRAIN-001 --input ./examples/sample_input
```

### 3) Create a synthetic training image (container)
```bash
python -m zd_drt make-image --cases-dir ./cases --case-id ZD-TRAIN-001
```

### 4) Simulate deletion (metadata only)
```bash
python -m zd_drt simulate-delete --cases-dir ./cases --case-id ZD-TRAIN-001 --image-name training_image.tar.gz --match "docs/*"
```

### 5) Restore simulated-deleted (extract from synthetic container to working/)
```bash
python -m zd_drt restore-simulated --cases-dir ./cases --case-id ZD-TRAIN-001 --image-name training_image.tar.gz --match "docs/*"
```

### 6) Verify integrity (evidence + synthetic container)
```bash
python -m zd_drt verify --cases-dir ./cases --case-id ZD-TRAIN-001
```

### 7) Generate a report pack
```bash
python -m zd_drt report --cases-dir ./cases --case-id ZD-TRAIN-001
# Optional PDF:
python -m zd_drt report --cases-dir ./cases --case-id ZD-TRAIN-001 --pdf
```

## CLI Commands
- `init-case`
- `ingest`
- `make-image`
- `simulate-delete`
- `restore-simulated`
- `verify`
- `report`
- `exercises`

For full options:
```bash
python -m zd_drt <command> --help
```

## Case folder structure
```
cases/<case_id>/
  evidence/
  working/
  exports/
  reports/
  logs/
  case.json
```

## Exercises
List exercises:
```bash
python -m zd_drt exercises list
```

Run a full guided lab (creates its own case):
```bash
python -m zd_drt exercises run --cases-dir ./cases --case-id ZD-LAB-001 --analyst "Instructor" --auth "Authorized lab run"
```

See `INSTRUCTOR_GUIDE.md` for a 60-minute lab plan.
