
███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║

# Zeid Data - Copper Hang Back...

# HOWTO — Zeid Data Exfiltration Monitor (Splunk App)

This guide walks you through **installing, validating, tuning, and enabling** the app’s detections safely.

---

## 1) Install the app

### Option A — Install ZIP (recommended)
1. In Splunk: **Apps → Manage Apps → Install app from file**
2. Select the provided ZIP
3. Restart Splunk if prompted

### Option B — Install from filesystem (Splunk Enterprise)
1. Unzip so you have a folder named: `ZeidData_Exfil_Monitor`
2. Copy to: `$SPLUNK_HOME/etc/apps/`
3. Restart Splunk

---

## 2) Validate prerequisites (CIM coverage)

This app is designed around CIM data models. You’ll get the best results if these are true:

### Network_Traffic
- You have outbound bytes (usually `bytes_out`) and at least:
  - `src`, `dest`, and ideally `dest_port` and `app`

### Web.Proxy
- You have:
  - `bytes_out`, `src`, `user`, and `url_domain` (or equivalent)

### DNS
- You have:
  - `query` and `src`

### Authentication
- You have:
  - successful auth actions mapped (e.g., `action=success`), plus `user` and `src`

**Quick checks (in Search)**
- Network data model availability:
  - `| tstats count from datamodel=Network_Traffic.All_Traffic where earliest=-24h latest=now`
- Proxy data model availability:
  - `| tstats count from datamodel=Web.Proxy where earliest=-24h latest=now`
- DNS data model availability:
  - `| tstats count from datamodel=DNS where earliest=-24h latest=now`
- Auth data model availability:
  - `| tstats count from datamodel=Authentication where earliest=-24h latest=now`

If a model returns 0 consistently, you either have no data, or it isn’t CIM-mapped.

---

## 3) Open dashboards first (no alerts yet)

Go to:
**Apps → Zeid Data | Exfiltration Monitor**

Start here before enabling anything:
- **ZD Exfil Overview** (sanity checks)
- **Cloud Uploads** (confirm `url_domain` and bytes)
- **DNS Anomalies** (confirm DNS logging exists)
- **Rare Destinations** (needs history for baseline)

---

## 4) Tune macros (make it fit your environment)

Open:
`ZeidData_Exfil_Monitor/default/macros.conf`

**Best practice**: copy any edits into:
`ZeidData_Exfil_Monitor/local/macros.conf`  
(so upgrades don’t overwrite your changes)

### Recommended initial tuning
- `zd_exfil_threshold_gb`
  - Start at **5–20 GB/hour** (depends on environment)
- `zd_exfil_threshold_mb_cloud`
  - Start at **250–2000 MB/30m**
- `zd_cloud_storage_domain_regex`
  - Add the storage domains you care about (or remove ones you don’t)

Business hours:
- `zd_exfil_business_hours_start` / `zd_exfil_business_hours_end`
  - Set these to your normal hours so “off-hours spike” is meaningful

---

## 5) Add allowlists (reduce noise fast)

Edit:
`lookups/zeid_exfil_dest_allowlist.csv`

Use:
- `dest_ip` for known-good external IPs (backup providers, SaaS egress points)
- `dest_domain` for known-good domains (enterprise file-sharing, approved vendors)

**Tip**: add comments so your future self knows why it’s allowed.

---

## 6) Enable detections safely (one-by-one)

All detections ship disabled.

In Splunk:
**Settings → Searches, reports, and alerts**

Filter by:
`ZD Exfil -`

Enable in this order (lowest risk → highest noise):

1. **High outbound bytes per source**
2. **Off-hours outbound spike**
3. **Large egress to cloud storage**
4. **High volume over file-transfer ports**
5. **DNS tunneling heuristics**
6. **Auth then egress chaining**
7. **Rare destination per source (7d baseline)**
8. **New geo for outbound destination**

After enabling each, run it manually and validate results.

---

## 7) What “good” looks like (triage checklist)

When something fires, ask:

### A) Is it expected?
- Scheduled backup?
- Known system doing replication?
- Approved cloud storage usage?

### B) Who/what is the source?
- Workstation vs server
- Privileged admin host
- Service account vs human user

### C) Where is it going?
- Known vendor / SaaS / CDN
- Newly registered domain
- Unfamiliar country (be careful: CDNs can mislead)

### D) What’s the method?
- Proxy/cloud upload (web gateway)
- File transfer ports (SFTP/FTP/SMB/WebDAV/NFS)
- DNS anomalies (possible tunneling)

### E) Do we have corroboration?
- Endpoint alerts
- DLP signals
- New process spawning network connections
- Unusual auth + network chaining

---

## 8) Common tuning patterns

### Too many alerts: “High outbound bytes”
- Raise `zd_exfil_threshold_gb`
- Add allowlists for known good destinations
- Split by asset class (servers vs endpoints) with separate searches (optional)

### Cloud uploads too noisy
- Tighten `zd_cloud_storage_domain_regex`
- Raise `zd_exfil_threshold_mb_cloud`
- Allowlist your sanctioned file-sharing provider(s)

### DNS tunneling detection too noisy
- Increase unique query threshold
- Exclude known telemetry domains (security tools often generate noisy DNS)
- Focus on unusual TLDs or high-entropy subdomains (advanced)

---

## 9) Troubleshooting

### Dashboards show “No results”
- Confirm data models return counts (Section 2)
- Expand time range to 7d to confirm history exists
- Check if your environment uses different fields (no CIM mapping)

### Saved searches fail with “Unknown savedsearch”
- You may have not restarted Splunk after installation
- Or the app is not visible to your role (check permissions)

### `tstats` returns 0 but raw searches return data
- CIM data model acceleration not enabled or not populated
- You may be missing CIM field extractions / tags / eventtypes

---

## 10) Optional: Splunk Enterprise Security (ES)

If you use Splunk ES:
- Convert these into correlation searches / notable rules.
- Use the app’s allowlist lookup as a suppression list.
- Consider adding risk scoring to sources/users for higher-fidelity triage.

---

## 11) Support / roadmap ideas (optional)
If you want to extend this skeleton:
- Add per-user and per-host baselines (median + MAD)
- Add summary indexing for faster dashboards
- Add “Top egress destinations” enrichment
- Add DLP / CASB / SaaS audit log correlation
- Add Watchlists (VIP users, crown jewel servers)

---
© Zeid Data. Defensive monitoring only.
