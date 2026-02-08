# HOWTO — CrowdStrike (Endpoint detections + dashboards)

1) Run `event_search/01_dns_requests.fql` to confirm visibility of DomainName + process attribution.
2) Use `03_suspected_api_usage.fql` to separate likely API usage from browsers.
3) Build widgets following `dashboards/claude_dashboard_spec.md`.
4) Operationalize with scheduled hunts per `reports/scheduled_hunts.md`.
