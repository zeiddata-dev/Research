# Instructor Guide — Zeid Data DRT (60-minute lab)

**Authorized training use only. Do not use on systems or data you do not own or have explicit permission to analyze.**

## Learning objectives
By the end of this lab, trainees can:
1) Initialize a case using a standard folder structure
2) Ingest evidence from a training dataset without altering the source
3) Produce file hashes and an evidence manifest (JSON + CSV)
4) Maintain a tamper-evident chain-of-custody log (hash chain)
5) Create and verify a synthetic training container
6) Simulate deletion and restore **only from the synthetic container**
7) Produce an audit-friendly report pack

## Suggested flow (60 minutes)
### 0–5 min — Setup
- Confirm Python 3.11+ is installed.
- Review the safety banner and scope in `SECURITY.md`.

### 5–15 min — Case creation and evidence intake
Run:
```bash
python -m zd_drt init-case --cases-dir ./cases --case-id ZD-LAB-001 --analyst "Trainee" --auth "Authorized lab run"
python -m zd_drt ingest --cases-dir ./cases --case-id ZD-LAB-001 --input ./examples/sample_input
```
Discuss:
- Why we ingest by copying into `evidence/`
- Why we hash and generate manifests

### 15–25 min — Hash verification & tamper simulation (safe)
Run:
```bash
python -m zd_drt verify --cases-dir ./cases --case-id ZD-LAB-001
python -m zd_drt exercises run-tamper --cases-dir ./cases --case-id ZD-LAB-001
```
Discuss:
- What a mismatch means
- Why we don't edit evidence

### 25–40 min — Synthetic training image + simulated deletion/restore
Run:
```bash
python -m zd_drt make-image --cases-dir ./cases --case-id ZD-LAB-001
python -m zd_drt simulate-delete --cases-dir ./cases --case-id ZD-LAB-001 --image-name training_image.tar.gz --match "docs/*"
python -m zd_drt restore-simulated --cases-dir ./cases --case-id ZD-LAB-001 --image-name training_image.tar.gz --match "docs/*"
```
Discuss:
- Why “deletion” is metadata-only here
- Restore = extraction from *known synthetic* container

### 40–50 min — Corrupted container scenario
Run:
```bash
python -m zd_drt exercises run-corrupt-container --cases-dir ./cases --case-id ZD-LAB-001
```
Discuss:
- Checksums and integrity of containers

### 50–60 min — Reporting
Run:
```bash
python -m zd_drt report --cases-dir ./cases --case-id ZD-LAB-001
```
Review the report sections and chain-of-custody entries.

## Assessment checklist
- Case created with required metadata
- Evidence manifest produced and verified
- Chain-of-custody includes at least 5 meaningful entries
- Synthetic image created, verified, and used for simulated deletion/restore
- Final report pack generated
