# Zeid Data — Topic Report Pack

**Date:** 2026-02-10  
**What this is:** a bundle of detection-forward research reports. Each file is a standalone .md you can publish as-is or split into repo docs.

## Contents
- `zeid_data_akira_ransomware_detection_report.md`
- `zeid_data_cl0p_data_extortion_detection_report.md`
- `zeid_data_qilin_extortion_detection_report.md`
- `zeid_data_safepay_ransomware_detection_report.md`
- `zeid_data_black_basta_detection_report.md`
- `zeid_data_cve_2026_21509_office_bypass_detection_report.md`
- `zeid_data_cve_2025_8110_gogs_rce_detection_report.md`
- `zeid_data_cve_2025_22225_vmware_esxi_detection_report.md`
- `zeid_data_cve_2025_68645_zimbra_rfi_detection_report.md`
- `zeid_data_cve_2025_34026_versa_concerto_auth_bypass_detection_report.md`

## Suggested repo moves
- `docs/reports/` → drop all .md files here
- `detections/` → turn the “Quick queries” into real:
  - `splunk/`
  - `sentinel_kql/`
  - `sigma/`
  - `suricata/`
- `dashboards/` → saved searches + screenshots + JSON exports where possible
- `tools/` → synthetic generator + baseline calculators

## Bro rules (so we don’t get cooked)
- No exploit PoCs. No weaponized steps. We hunt **telemetry**.
- Always baseline by **role** (server vs workstation vs SaaS admin).
- Evidence-first: every alert should spit out a **receipt bundle**.
