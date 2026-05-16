<!-- ZEID DATA README BANNER START -->
<p align="center">
  <img src="../../../media/readme_banners/content_splunk_zeid_data_claude_bot_content.svg" alt="Splunk · Zeid Data Claude Bot Content banner" width="100%">
</p>
<!-- ZEID DATA README BANNER END -->

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
