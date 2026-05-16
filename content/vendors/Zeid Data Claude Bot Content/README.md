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

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![content](https://img.shields.io/badge/content-334155?style=flat-square) ![vendor-content](https://img.shields.io/badge/vendor%20content-334155?style=flat-square) ![governance](https://img.shields.io/badge/governance-6F42C1?style=flat-square) ![evidence-assets](https://img.shields.io/badge/evidence%20assets-334155?style=flat-square) ![vendors](https://img.shields.io/badge/vendors-334155?style=flat-square) ![zeid-data-claude-bot-content](https://img.shields.io/badge/zeid%20data%20claude%20bot%20content-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Splunk — Claude/Anthropic (Firewall + Endpoint) pack

Included:
- lookup: `lookups/claude_domains.csv`
- searches: `spl/`
- dashboard: `dashboards/claude_firewall_endpoint_dashboard.xml`
- ES examples: `splunk_es/savedsearches.conf`
- reporting notes: `reports/report_searches.md`

Assumptions:
- firewall logs in `index=firewall`
- endpoint logs (CrowdStrike example) in `index=crowdstrike`
Adjust SPL to your environment.
