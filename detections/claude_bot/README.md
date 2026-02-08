# Claude Bot Detection (Quick Guide)

This folder contains simple, vendor-agnostic guidance to **spot and validate Claude (Anthropic) web/app traffic** using the telemetry you already collect (DNS, TLS, proxy, firewall, EDR).

## What you can reliably detect
Claude usage usually appears as:
- **Outbound HTTPS (443)** to Anthropic/Claude-related domains
- **DNS lookups** for Claude/Anthropic domains
- **TLS SNI / certificate metadata** that matches the destination
- **Proxy/Firewall URL categories** related to “AI/Chat” or “Productivity”

> Note: Exact domains and IPs can change. Prefer **domain + TLS + egress patterns** over static IP allow/deny lists.

## Data sources to use
- **DNS logs** (resolver, secure DNS, network sensor)
- **Proxy / SWG logs** (URL, category, user/device)
- **Firewall logs** (egress 443, destination, bytes)
- **TLS handshake telemetry** (SNI, JA3/JA4 if available)
- **Endpoint telemetry** (process + network connections, browser extension events)

## Quick detection logic (plain English)
Flag sessions where a user/device:
1) Resolves a Claude/Anthropic domain (DNS), then  
2) Connects outbound 443 to that destination (firewall/proxy), and  
3) TLS SNI/cert aligns to the same domain (TLS telemetry)

Enrich with:
- user, device, asset group (corp vs BYOD)
- geolocation (unexpected regions)
- volume anomalies (large uploads, sustained sessions)

## Minimal rules you can implement
- **DNS rule:** alert on queries matching `*claude*` or `*anthropic*` (case-insensitive), excluding known-approved devices/users.
- **Proxy rule:** alert on AI-chat categories OR URL host contains `claude` / `anthropic`.
- **Firewall rule:** correlate DNS → egress 443 within 5 minutes for the same client.
- **EDR rule (optional):** browser process with repeated connections to Claude/Anthropic domains during restricted hours or from restricted hosts.

## Validation checklist (avoid false positives)
- Confirm destination via **TLS SNI/cert subject** (not just IP)
- Confirm the **same client** did DNS + egress
- Check whether traffic is **corporate-approved** (policy exception list)
- Distinguish “open page once” vs **sustained usage / uploads**

## Response playbook (lightweight)
- **Low severity:** notify user, log the event, verify business justification
- **Medium:** require approved account, enforce proxy policy, restrict uploads
- **High:** investigate data exfil risk (large uploads, sensitive host), isolate device if needed

## Recommended output fields
Store these for audit-ready reporting:
- timestamp, user, device, src_ip, dest_domain, dest_ip
- proxy action (allow/block), url_category
- tls_sni, cert_subject (if available)
- bytes_out, bytes_in, duration
- policy decision + ticket/approval reference

## Disclaimer
This repo provides **defensive detection guidance** only. Always follow your organization’s acceptable-use, privacy, and monitoring policies.
