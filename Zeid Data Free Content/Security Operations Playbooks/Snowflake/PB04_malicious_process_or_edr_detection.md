# Zeid Data Security Playbooks — Snowflake — Malicious Process or EDR Detection

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Playbook ID:** SNO-PB04  
**Vendor:** Snowflake  
**Last updated:** 2026-02-08

---
## Purpose

Triage malicious process alerts or endpoint detections; isolate and remediate.

## Trigger and severity

**Triggers (examples):**
- SIEM alert/correlation search fires for **malicious process or edr detection**
- Vendor alert/finding indicates suspicious activity matching this scenario
- Analyst observation during proactive hunting

**Severity (default):** Medium  
**Target MTTR:** 8h

## Required telemetry assumptions

**Assumed log sources / telemetry (make assumptions):**
- LOGIN_HISTORY
- QUERY_HISTORY
- ACCESS_HISTORY (if enabled)
- ACCOUNT_USAGE views

**Minimum fields to capture for pivots:**
- timestamp (UTC), user/account, source IP, destination, action/result, device/host (if applicable)
- alert/finding IDs, tenant/workspace identifiers, and policy names (if applicable)

**Vendor note:** Snowflake playbooks focus on query patterns, data unloads, role changes, and network policies.

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
index=snowflake* sourcetype=snowflake:* (process_name OR Image OR CommandLine OR detection)
| stats count values(process_name) as procs values(dest) as hosts by user
```

**Sentinel (example):**

```kusto
DeviceProcessEvents
| where InitiatingProcessCommandLine has_any ("powershell", "rundll32", "wscript", "mshta")
| project TimeGenerated, DeviceName, AccountName, FileName, ProcessCommandLine
```

> Scope queries to approved indexes/tables in your environment.

## Post-incident

- Root cause summary (how it happened)
- Control gaps and recommended fixes
- Detection tuning notes
- Lessons learned; update playbook as needed

