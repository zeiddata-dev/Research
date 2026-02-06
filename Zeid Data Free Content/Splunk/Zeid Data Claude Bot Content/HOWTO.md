# HOWTO — Splunk (Firewall + Endpoint dashboards)

1) Upload lookup `lookups/claude_domains.csv`.
2) Update SPL field names to match your firewall + endpoint schemas.
3) (Recommended) Create `host_ip_lookup.csv` (ComputerName, src_ip) for correlation.
4) Create a new Splunk dashboard and paste `dashboards/claude_firewall_endpoint_dashboard.xml`.
5) Turn key SPL into scheduled alerts or ES correlation searches.
