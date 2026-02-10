# Zeid Data Research Report — CVE-2025-22225 (2025–2026): VMware ESXi arbitrary write — ransomware-linked exploitation signals

**Version:** 0.1
**Date:** 2026-02-10 (America/Chicago)
**Owner:** Zeid Data Research Labs
**Vibe:** evidence-first, detections-forward — *if it didn’t generate evidence, it didn’t happen.*

---

## 1) What this is (in plain words)
- CVE-2025-22225 is part of a VMware ESXi/Workstation/Fusion vulnerability trio; reporting notes CISA updated KEV to confirm ransomware use and that exploitation toolkits were observed in January 2026.
-
-

## 2) Why it matters (threat + business risk)
- **Threat:** attackers want speed + scale + leverage (data theft, downtime, extortion).
- **Business hit:** outage, regulatory exposure, brand damage, and expensive incident response.
- **Research payoff:** this topic produces **repeatable network detections** you can validate in any enterprise/hybrid environment.

## 3) Threat model (what the attacker wants)
- **Attacker goal:** get foothold → escalate → move laterally → exfiltrate → disrupt / extort.
- **Constraints (defender advantage):**
  - They *must* talk on the wire (DNS/TLS/HTTP/flows).
  - They *must* touch identity (auth, tokens, admin actions).
  - They *must* stage data somewhere before it leaves.

## 4) Minimum telemetry (MVP) + nice-to-have
**MVP (don’t argue, just ship):**
- DNS logs (queries + responses, client IP/user/host)
- TLS metadata (SNI/ALPN/cert, JA3/JA4 if you have it)
- HTTP/proxy logs (host, URL path, bytes, user agent)
- NetFlow/IPFIX (src/dst/bytes/duration)
- Identity logs (SSO, MFA, OAuth consent, admin actions)
- Endpoint network events (process → destination, if available)

**Nice-to-have (makes your detections nasty):**
- EDR process lineage + command-line
- Email security logs (attachments, URL rewrites, click logs)
- SaaS audit logs (M365, Google Workspace, Okta, Slack, GitHub, etc.)
- Firewall policy change logs / ZTNA broker logs

## 5) Detection ideas (Zeid Data-style “receipts”)
### 5.1 Core hypotheses to test
- H1: This activity creates **role-mismatch** network behavior (a “boring server” starts acting like a client).
- H2: The attack produces **rare destinations** + **rare protocols/JA3** compared to baseline.
- H3: Identity and network anomalies cluster tightly in time (minutes to hours).

### 5.2 High-signal detections (vendor-agnostic)
- Management plane exposure: alert on any internet-exposed ESXi/Workstation services and inbound from untrusted geos; treat as 'stop-the-line'.
- East-west blast radius: after compromise, expect rapid SMB/RDP/SSH movement from virtualization admin segments into file/backup domains.
- Backups get hit: monitor for sudden auth failures/successes to backup consoles plus deletion/disable events.

### 5.3 Quick queries (starter templates)
**Splunk-ish (pseudo):**
```spl
| tstats sum(bytes_out) as bytes_out, dc(dest_ip) as uniq_dests from datamodel=Network_Traffic where earliest=-24h latest=now by src_host, user
| where bytes_out > (baseline_p95 * 3) OR uniq_dests > (baseline_p95_uniq * 3)
| sort - bytes_out
```

**Sentinel KQL-ish (pseudo):**
```kusto
let lookback=24h;
NetworkTraffic
| where TimeGenerated > ago(lookback)
| summarize bytes_out=sum(BytesSent), uniq_dests=dcount(DestinationIP) by SrcHost, User, bin(TimeGenerated, 1h)
| where bytes_out > 3*percentile(bytes_out, 95) or uniq_dests > 3*percentile(uniq_dests, 95)
```

**Suricata rule sketch (metadata-only focus):**
```text
# Not a signature for "the exploit". A signature for "this server should not be doing that much outbound."
# Build on SNI/host/JA3 baselines + bytes thresholds in your NDR instead of pretending DPI solves it.
```

## 6) Evaluation plan (how you prove it works)
- **Datasets:** your own org logs + synthetic generator (below) + a small “benign baseline week”.
- **Baselines:** per-host/per-role baselines (mail server vs dev laptop vs VPN concentrator).
- **Metrics:** precision/recall, alert volume per day, mean-time-to-triage, top FP drivers.
- **FP drivers to watch:** backups, software updates, new SaaS rollouts, IT migrations, legit remote support tools.

## 7) Synthetic data plan (safe + reproducible)
- Generate **fake** DNS/TLS/HTTP/flow records that mimic the behaviors above.
- Feed into: Splunk ingest, Sentinel workspace, Elastic, or just CSV for dashboards.
- Keep it defensive: no exploit payloads, no weaponized instructions — just **telemetry-shaped events**.

**Generator idea (repo deliverable):**
- `tools/synth_gen.py` outputs JSONL for:
  - DNS query bursts
  - rare SNI + long-lived TLS sessions
  - big outbound flows from “server roles”
  - identity anomalies (new device, MFA reset, OAuth consent)

## 8) Evidence bundle (audit-ready)
When the alert fires, your “Zeid Data receipts” should include:
- 24–72h timeline of DNS/TLS/HTTP/flows for the host(s)
- identity events for the user/service accounts involved
- endpoint network lineage (process → dest) if you have it
- config change logs (firewall, ZTNA, IdP, SaaS)
- notes: “what we saw / what we ruled out / what we did next”

## 9) 2-week sprint plan (Day 1–14)
- **Day 1:** lock scope, define target roles (servers/users) + success metrics.
- **Day 2:** baseline queries (top talkers, rare domains, rare JA3/JA4).
- **Day 3:** draft 5–8 detections (MVP) + FP notes.
- **Day 4:** build dashboards (bytes out, rare dests, identity anomalies).
- **Day 5:** build synthetic generator v0 (JSONL/CSV).
- **Day 6:** run replay tests on 7 days benign baseline; tune thresholds.
- **Day 7:** add “triage helper” outputs (who/what/when/where).
- **Day 8:** add rule-pack outputs (Sigma + Splunk + KQL placeholders).
- **Day 9:** write README + HOWTO (how to deploy + how to validate).
- **Day 10:** add “evidence bundle template” (markdown checklist).
- **Day 11:** red-team *simulation* (safe): replay synthetic data into SIEM; measure alerting.
- **Day 12:** document FP drivers + suppression strategy.
- **Day 13:** polish visuals (dashboard screenshots or mockups).
- **Day 14:** publish: GitHub repo + writeup + short LinkedIn “free content drop”.

## 10) Publishability + Buildability (Zeid Data gut check)
- **Publishability:** 8/10 — strong story, actionable detections, portable to most orgs.
- **Buildability:** 8/10 — single engineer can ship MVP in 2 weeks with synthetic support.

## 11) Sources (receipts)
- [Help Net Security: KEV ransomware flag & exploitation observations (Feb 5, 2026)](https://www.helpnetsecurity.com/2026/02/05/cisa-cve-2025-22225-ransomware-exploitation/)

---
*Zeid Data Research Labs — ship detections, ship receipts, stay audit-ready.*