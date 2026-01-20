# Zeid Data - Copper Hang Back...
# HOWTO — Deploy & Use the SOC 2 Evidence Workbook (Sentinel Multi‑Source)

This guide walks you through:

1. Preparing your data sources
2. Importing or deploying the workbook
3. Validating the panels
4. Exporting evidence for SOC 2
5. Customizing for your table names / schema

---

## 1) Prerequisites

### Permissions

You’ll typically need:

- **Microsoft Sentinel Contributor** *(or equivalent)* to save workbooks in Sentinel
- **Log Analytics Reader** *(or higher)* on the workspace to run queries

### Data connectors (high level)

Enable and validate ingestion for:

- **Entra ID**: Sign-in logs + Audit logs
- **M365**: Unified audit log → `OfficeActivity`
- **AWS**: CloudTrail (and optionally GuardDuty)
- **Okta**: System Log
- **CrowdStrike**: detections/alerts via the connector you use
- **Cisco**: CEF via AMA/Legacy agent → `CommonSecurityLog`

> The workbook works best when each source is consistently ingested into *one* workspace during the evidence window.

---

## 2) Import the workbook (Portal)

1. Go to **Microsoft Sentinel** → **Workbooks**
2. Click **+ Add workbook**
3. Click **Edit**
4. Open **Advanced Editor**
5. Paste the contents of `sentinel_soc2_workbook_multi_source.workbook`
6. Click **Apply**
7. Click **Save**

---

## 3) Deploy the workbook (ARM)

Use `sentinel_soc2_workbook_multi_source_arm.json` if you want infrastructure-as-code.

### Option A — Azure Portal deployment

1. Azure Portal → **Deploy a custom template**
2. Upload `sentinel_soc2_workbook_multi_source_arm.json`
3. Set parameters:
   - `workbookDisplayName`: name shown in Workbooks
   - `workbookSourceId`: **Resource ID** of the Log Analytics workspace

**Workspace resource ID example**:

`/subscriptions/<subId>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspaceName>`

### Option B — Azure CLI (example)

```bash
az deployment group create \
  --resource-group <rg> \
  --template-file sentinel_soc2_workbook_multi_source_arm.json \
  --parameters workbookDisplayName="SOC 2 Compliance Evidence (Multi-Source)" \
              workbookSourceId="/subscriptions/<subId>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspaceName>"
```

---

## 4) Validate ingestion (before you trust exports)

### A) Use the Overview → Source continuity panel

- Look for **LastSeen** timestamps per table.
- Confirm each source has events in the time window.

### B) Quick KQL spot checks

Run these in Logs (adjust timeframe as needed):

```kusto
SigninLogs | take 5
AuditLogs | take 5
OfficeActivity | take 5
union isfuzzy=true AWSCloudTrail, AWSCloudTrail_CL | take 5
union isfuzzy=true OktaSystemLogs, Okta_CL | take 5
CrowdStrikeDetections | take 5
CommonSecurityLog | take 5
```

If any query errors with “table not found”, your connector is either not enabled or writing to a different table name.

---

## 5) Operating the workbook for SOC 2 evidence

### Recommended monthly evidence routine

1. Set **TimeRange** to the month (or audit period slice).
2. Capture screenshots of:
   - Overview (incidents, alerts by provider, last-seen)
   - Identity & Access (role/policy changes)
   - Monitoring & IR (MTTC/backlog)
3. Go to **Evidence Export** tab.
4. Export the consolidated timeline to CSV.
5. Attach required supporting artifacts:
   - Access reviews/approvals (tickets)
   - Change approvals (PRs/CAB)
   - Retention configuration evidence
   - Incident postmortems (if applicable)

### Break-glass spotlight

Populate the **BreakGlassUPNs** parameter (comma-separated), then review the Identity tab.

---

## 6) Customize for your environment

### A) If a vendor uses different tables

Common variants:

- Okta
  - Preferred: `OktaSystemLogs`
  - Legacy/custom: `Okta_CL`

- AWS
  - Preferred: `AWSCloudTrail`
  - Legacy/custom: `AWSCloudTrail_CL`

- CrowdStrike
  - If you’re using a connector that lands in custom tables (e.g., via FDR or a data collector), rename `CrowdStrikeDetections` in the workbook to your table.

To change a table name:

1. Open the workbook → **Edit**
2. Select the panel → edit query
3. Replace the table name in the KQL
4. **Apply** and **Save**

### B) Tune Cisco filtering

The Cisco panels filter on:

- `DeviceVendor` contains “Cisco”, or
- `DeviceProduct` contains “Cisco” or includes `ASA`, `Firepower`, `Umbrella`

If your logs populate different values, adjust the filter clause:

```kusto
| where DeviceProduct in~ ("<your exact product name>")
```

### C) Tune M365 operations list

The M365 panel uses a **high-signal** operation list (mailbox rules, permissions, transport rules, role assignment changes). If your auditor focuses on different actions, modify the `Operation has_any (...)` list.

---

## 7) Evidence handling tips

- Export CSVs to a controlled location (restricted access).
- Consider a standardized “Evidence Bundle” naming convention:
  - `SOC2_<YYYY-MM>_<Source>_<Workspace>.csv`
- If you share with an auditor, decide whether to:
  - provide raw CSVs, or
  - provide summarized exports + redacted raw events upon request

---

## 8) Troubleshooting

### “Failed to resolve table”

- Connector not enabled, not configured correctly, or data hasn’t arrived.
- Fix by enabling connector, validating permissions, and verifying table name.

### Empty results

- Expand **TimeRange**.
- Confirm the selected workspace is receiving the logs.

### SentinelHealth empty

- Health monitoring may not be enabled or supported in your setup.
- You can remove the panel or leave it as optional.

---

## 9) What to do next (common enhancements)

If you want to take this from “evidence dashboard” → “audit pack machine”:

- Add a **Control Coverage** tab (your internal controls list + evidence links)
- Add **Watchlists** (break-glass accounts, privileged users, crown-jewel assets)
- Add **Change ticket correlation** (if you ingest ServiceNow/Jira change events)
- Add **Data retention checks** (document retention settings and attach configuration exports)

