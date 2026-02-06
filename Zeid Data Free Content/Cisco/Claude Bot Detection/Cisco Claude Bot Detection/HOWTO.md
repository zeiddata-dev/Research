# HOWTO — Cisco (Firewall + IPS) detection for Claude/Anthropic

## 1) Deploy FQDN/URL objects
- Create objects for domains in `indicators/domains.txt`
- Add an Access Control policy rule:
  - ALLOW (detection mode)
  - Log at beginning + end

## 2) Deploy Snort 3 SNI rules (recommended)
- Import `snort3/claude_sni.rules`
- Set action: ALERT
- Verify IPS events when a client reaches `claude.ai`

## 3) Export logs for dashboards
Forward firewall + IPS events to your SIEM for dashboards and endpoint correlation.

## 4) Validate
From a test client:
- Browse to `https://claude.ai`
- Confirm firewall rule hit and (if enabled) Snort alert.
