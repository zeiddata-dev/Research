# Zeid Data Security Playbooks — Databricks — Command and Control Beaconing

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Playbook ID:** DAT-PB06  
**Vendor:** Databricks  
**Last updated:** 2026-02-08

---
## Purpose

Identify possible C2 activity via repetitive network beacons or known-bad indicators.

## Trigger and severity

**Triggers (examples):**
- SIEM alert/correlation search fires for **command and control beaconing**
- Vendor alert/finding indicates suspicious activity matching this scenario
- Analyst observation during proactive hunting

**Severity (default):** High  
**Target MTTR:** 4h

## Required telemetry assumptions

**Assumed log sources / telemetry (make assumptions):**
- Workspace audit logs (cluster/job/notebook events)
- Token/PAT events (where logged)
- Access events for external locations (if used)

**Minimum fields to capture for pivots:**
- timestamp (UTC), user/account, source IP, destination, action/result, device/host (if applicable)
- alert/finding IDs, tenant/workspace identifiers, and policy names (if applicable)

**Vendor note:** Databricks playbooks focus on workspace admin events, cluster/job activity, and data access patterns.

## Triage steps

1. **Confirm scope & authorization**
   - Confirm you are authorized for this case/scope and log sources.

2. **Validate alert quality**
   - Review context, timestamps, and whether prevention occurred.
   - Identify expected activity that could explain the signal.

3. **Establish a timeline**
   - First seen / last seen
   - Expand window (±24h) if needed for related activity.

4. **Pivot on key entities**
   - user/account → other logins/actions
   - host/device → process tree / network connections (if available)
   - IP/domain → other affected users/hosts

5. **Determine impact**
   - Was access gained? Were privileges changed? Was data accessed/exfiltrated?
   - Identify affected systems and datasets.

## Containment

**Containment options (least-disruptive first):**
- Disable/reset credentials for confirmed compromised accounts
- Revoke tokens/keys/sessions where supported
- Isolate endpoint(s) if malicious execution is confirmed (EDR action)
- Block IOCs at DNS/Proxy/Firewall/EDR where appropriate
- Tighten conditional access/policies during active abuse

**Decision points:**
- If **active exploitation** is confirmed → escalate and contain immediately.
- If **data exposure** is suspected → preserve evidence and notify stakeholders per policy.

## Eradication

- Remove confirmed persistence (tasks, startup items, OAuth grants, access keys)
- Patch misconfigurations/vulnerabilities that enabled access
- Rotate credentials/keys and invalidate sessions
- Validate with rescans / follow-up hunting

## Recovery

- Restore normal access with least privilege
- Re-enable accounts only after rotations and policy review
- Monitor for recurrence (7–14 days watchlist)

## Evidence to capture

**Capture and store (evidence-first):**
- Alert/finding details (IDs, raw JSON if available)
- Relevant log exports in original format (UTC)
- Hashes/manifests of exported artifacts
- Chain-of-custody entries (who/what/when/where)
- Screenshots/PDFs of key console views (if allowed)

## Queries

### Queries and pivots

**Splunk (example):**

```spl
index=databricks* sourcetype=databricks:audit (dest_port=443 OR dest_port=80)
| stats count as hits dc(_time) as intervals by src_ip, dest_ip, dest_port
| where hits > 200
```

**Sentinel (example):**

```kusto
DeviceNetworkEvents
| where RemotePort in (80,443)
| summarize hits=count() by DeviceName, RemoteIP, RemotePort, bin(TimeGenerated, 5m)
| where hits > 200
```

> Scope queries to approved indexes/tables in your environment.

## Post-incident

- Root cause summary (how it happened)
- Control gaps and recommended fixes
- Detection tuning notes
- Lessons learned; update playbook as needed

