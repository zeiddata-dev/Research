# Zeid Data - Copper Hang Back...
# comments: deposit ghost trace (copper).
# SOC 2 Compliance Evidence — Microsoft Sentinel Workbook (Multi‑Source)

This repo artifact contains a Microsoft Sentinel / Log Analytics **workbook** designed to help you **collect and package SOC 2 evidence** across these sources:

- **Entra ID** (AuditLogs, SigninLogs)
- **Microsoft 365** (OfficeActivity)
- **AWS** (CloudTrail)
- **Okta** (Okta System Log)
- **CrowdStrike** (detections / alerts)
- **Cisco** (network/security device logs via CEF/Syslog → CommonSecurityLog)

> **Note:** SOC 2 is ultimately about *controls + evidence*. This workbook supports evidence collection and visibility, but it does not replace policies, approvals, ticketing, or auditor judgment.

---

## Files

- `sentinel_soc2_workbook_multi_source.workbook`
  - Workbook JSON you can import directly into Microsoft Sentinel Workbooks (Advanced Editor).
- `sentinel_soc2_workbook_multi_source_arm.json`
  - ARM template to deploy the workbook as an Azure resource (`Microsoft.Insights/workbooks`).

---

## What the workbook shows

### Tabs

- **Overview**
  - Incident summary
  - Alerts by provider/product/severity
  - **Data source continuity / last‑seen** across your SOC 2 log sources
  - Sentinel health (if `SentinelHealth` is enabled)

- **Identity & Access (Entra ID + Okta)**
  - Entra role assignment changes (privileged access)
  - Entra policy changes (Conditional Access / auth policies)
  - Okta system log recent activity
  - Optional break‑glass sign‑in spotlight

- **Microsoft 365 (OfficeActivity)**
  - High‑signal admin operations (mailbox rules, permissions, transport rules, etc.)
  - External sharing / link creation signals

- **AWS (CloudTrail)**
  - IAM / privilege changes
  - Root usage & console logins
  - Security logging changes (StopLogging, bucket policy / trail changes)

- **Endpoint & Network (CrowdStrike + Cisco)**
  - CrowdStrike detections summary + recent detections
  - Cisco CEF events + top blocked/denied actions

- **Monitoring & IR**
  - MTTC (mean/median/p90 time‑to‑close) by severity
  - Backlog trend
  - Work distribution by owner
  - Sentinel health (connectors / analytics / automation)

- **Evidence Export**
  - Consolidated, exportable timeline across all supported sources (incidents, Entra, M365, Okta, AWS, CrowdStrike, Cisco)

---

## Required data (tables)

The workbook is written to be **column-safe** and **table-safe** when possible:

### Primary tables

- Sentinel incidents & alerts
  - `SecurityIncident`
  - `SecurityAlert`

- Entra ID
  - `SigninLogs`
  - `AuditLogs`

- Microsoft 365
  - `OfficeActivity`

- Okta
  - `OktaSystemLogs` *(preferred)*
  - `Okta_CL` *(fallback for environments that ingest to a custom table)*

- AWS
  - `AWSCloudTrail` *(preferred)*
  - `AWSCloudTrail_CL` *(fallback custom table)*

- CrowdStrike
  - `CrowdStrikeDetections` *(used directly in multiple panels)*
  - (optional) `CrowdStrikeAlerts`, `CrowdStrikeIncidents`, `CrowdStrikeHosts`

- Cisco / network
  - `CommonSecurityLog` *(CEF)*
  - (optional) `Syslog`

If a vendor connector writes to **different custom tables** in your environment, you can adjust the queries (see HOWTO).

---

## Parameters

- **TimeRange**: evidence window (set it to your audit period / monthly evidence window)
- **Section**: tab selector
- **BreakGlassUPNs** *(optional)*: comma-separated UPN list to spotlight emergency access usage

---

## SOC 2 alignment (practical mapping)

This workbook is built to help you gather evidence commonly used for:

- **Security monitoring & incident response** (incidents, alerts, MTTC, backlog)
- **Logical access** (role/policy changes, sign-in failures, break-glass usage)
- **Change management** (AWS & M365 admin actions, CloudTrail logging changes)
- **Logging & monitoring continuity** (last-seen coverage across critical sources)

Your auditor may map these to Trust Services Criteria in different ways. Pair exports with:

- IR plan + on-call procedures
- Access review evidence (tickets/approvals)
- Change approvals (PRs/CAB/tickets)
- Retention configuration documentation

---

## Quickstart

1. Ensure connectors are enabled and data is flowing (Entra ID, OfficeActivity, AWS, Okta, CrowdStrike, Cisco CEF).
2. Import the workbook JSON (`.workbook`) into Sentinel Workbooks.
3. Set **TimeRange** to your evidence window.
4. Use **Evidence Export** tab → export to CSV for your audit packet.

For detailed steps, see **HOWTO.md**.

---

## Troubleshooting

- **“Failed to resolve table …”**
  - The connector isn’t enabled, data hasn’t arrived yet, or your environment uses a different table name.
  - Fix by enabling the connector or updating the query to your table name.

- **No results**
  - Expand **TimeRange**.
  - Confirm the workspace being queried is the one receiving the logs.

- **SentinelHealth is empty**
  - Health monitoring may not be enabled, or your tenant/workspace doesn’t emit that table.

---

## Security / privacy notes

- Evidence exports may contain usernames, IPs, and device names.
- Use least privilege when sharing exports.
- Consider redaction for auditor sharing if needed.

