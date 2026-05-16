<!-- ZEID DATA README HERO START -->
![Zeid Data content banner](../../../assets/banners/readme/content.png)

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../.."><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![content](https://img.shields.io/badge/content-334155?style=flat-square) ![vendor-content](https://img.shields.io/badge/vendor%20content-334155?style=flat-square) ![governance](https://img.shields.io/badge/governance-6F42C1?style=flat-square) ![evidence-assets](https://img.shields.io/badge/evidence%20assets-334155?style=flat-square) ![splunk](https://img.shields.io/badge/splunk-334155?style=flat-square) ![spl](https://img.shields.io/badge/spl-334155?style=flat-square) ![security-analytics](https://img.shields.io/badge/security%20analytics-334155?style=flat-square) ![vendors](https://img.shields.io/badge/vendors-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data | Exfiltration Monitor (Splunk App Skeleton)

A lightweight Splunk app skeleton to help you **detect and triage data exfiltration signals** using:
- **Dashboards** (SimpleXML) for high-signal views
- **Detections** (saved searches) you can schedule or convert into ES notables
- **Allowlists** (lookups) to suppress known-good destinations

> Ships **safe-by-default**: all detections are **disabled** (`enableSched=0`) until you enable and tune.

## What you get
### Dashboards
- **ZD Exfil Overview** – outbound spikes, off-hours spikes, file-transfer ports
- **Cloud Uploads** – large uploads to common cloud storage domains
- **DNS Anomalies** – tunneling heuristics (long queries / high unique volume)
- **Rare Destinations** – rare per-source destinations + new outbound geos

### Detections (saved searches)
- High outbound bytes per source
- Off-hours outbound spike
- Large egress to cloud storage
- High volume over file-transfer ports
- DNS tunneling heuristics
- Rare destination per source (7d baseline)
- New geo for outbound destination
- Privileged auth then egress chaining

## Requirements (recommended)
Best results when your data is **CIM mapped**:
- `Network_Traffic` (for bytes_out, dest, src, dest_port, app)
- `Web` / `Web.Proxy` (for bytes_out, url_domain, user)
- `DNS` (for query, src)
- `Authentication` (for action=success, user, src)

It can still work without CIM, but you’ll need to update macros/searches.

## Install
### Splunk Enterprise
1. Install the ZIP: **Apps → Manage Apps → Install app from file**
2. Restart Splunk if prompted.

### Splunk Cloud
- Install via the supported app install process for your tenant (self-service or support-assisted, depending on your plan).

## Quick start (10 minutes)
1. Open the dashboards: **Apps → Zeid Data | Exfiltration Monitor**
2. Confirm you see data (even if empty results at first).
3. Tune thresholds + domains in `macros.conf`:
   - `zd_exfil_threshold_gb` (default 5 GB/hour)
   - `zd_exfil_threshold_mb_cloud` (default 500 MB/30m)
   - `zd_cloud_storage_domain_regex`
4. Add known-good destinations to `lookups/zeid_exfil_dest_allowlist.csv`
5. Enable detections in **Settings → Searches, reports, and alerts** (filter `ZD Exfil -`).

## Tuning highlights
- **Start high, then lower**: begin with higher thresholds to avoid alert fatigue.
- **Allowlist aggressively**: backups, SaaS, CDN endpoints, approved file transfers.
- **Baseline by peer group**: servers vs workstations, IT admins vs standard users.
- **Reduce “geo” noise**: CDNs can introduce country variability.

## Safety & scope
- Defensive monitoring only.  
- Use in accordance with your organization’s policies and applicable laws.

## License
© Zeid Data. (Add your preferred license text if publishing publicly.)

## Need the step-by-step?
See **HOWTO.md** for validation, enablement workflow, and troubleshooting.
