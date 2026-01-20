# Zeid Data - Copper Hang Back..
# comments: deposit ghost trace (copper)
# AuditPack (Compliance Evidence Scanner)

AuditPack is a **policy-driven compliance scanner** whose primary goal is producing **audit-ready evidence**.

For each control in a policy file, AuditPack generates an **evidence bundle** folder containing:
- `raw/` (captured command outputs, file metadata, etc.)
- `normalized/control.json` (normalized JSON results)
- `NARRATIVE.md` (short narrative suitable for auditors)
- `TIMESTAMPS.json` (collection timestamps)
- `FILE_HASHES.sha256` + `CHAIN_OF_CUSTODY.json` (chain-of-custody metadata)

It then produces a single zipped **Audit Pack** containing all bundles plus an **executive summary**.

> ⚠️ **Security note:** This tool runs commands defined by your policy. Treat policies as code.

## Quick start

### 1) Install

```bash
pip install -e .
```

### 2) Run the sample policy

```bash
auditpack run --policy examples/policy.sample.yaml --out ./out
```

Outputs:
- `out/auditpack_<timestamp>/...` (audit pack folder)
- `out/auditpack_<timestamp>.zip` (zipped pack)
- `out/auditpack_<timestamp>.zip.sha256` (hash of the zip)

## CLI

```bash
auditpack run --policy POLICY.yaml [--out OUT_DIR] [--pack-name NAME] [--timeout-seconds 30]
```

Options:
- `--no-zip` : do not create a zip
- `--timeout-seconds` : default per-command timeout
- `--include-env` : include a sanitized environment snapshot in metadata

## Policy format (YAML)

Minimal:

```yaml
policy_version: "1.0"
pack:
  org: "Example Corp"
  system: "prod-payments"
  owner: "Security"
controls:
  - id: "LOG-01"
    name: "Centralized logging enabled"
    description: "Verify core logging services are enabled and config exists."
    mappings:
      SOC2: ["CC7.2", "CC7.3"]
      ISO27001: ["A.8.15", "A.8.16"]
      NISTCSF: ["DE.CM-1", "DE.CM-7"]
    evidence:
      - type: os_info
        id: "host_context"
      - type: command
        id: "journald_status"
        when: "linux"
        command: ["systemctl", "is-enabled", "systemd-journald"]
      - type: file_exists
        id: "inputs_conf_present"
        when: "linux"
        path: "/opt/splunkforwarder/etc/system/local/inputs.conf"
```

### Control mappings

Mappings are **first-class** in the policy file under `mappings:` and are carried into:
- per-control narratives
- normalized JSON
- executive summary rollups (counts per framework)

## Evidence bundle structure

```
controls/
  LOG-01__centralized-logging-enabled/
    raw/
      journald_status.stdout.txt
      journald_status.stderr.txt
      journald_status.meta.json
    normalized/
      control.json
    NARRATIVE.md
    TIMESTAMPS.json
    FILE_HASHES.sha256
    CHAIN_OF_CUSTODY.json
```

## Extending collectors

Built-in evidence collectors:
- `os_info` (hostname, OS, time, Python, tool version)
- `command` (runs a command and captures stdout/stderr/exit code)
- `file_exists` (presence + stat metadata)
- `file_hash` (SHA-256 of a file + metadata)

You can add new collectors by implementing `auditpack.collectors.base.Collector` and registering it in `auditpack.cli:COLLECTORS`.

## License

MIT
