# Cloaked Phishing via Server-Side Filtering
## Why “the scanner said it’s fine” is not a security strategy

**Author:** Zeid Data Research Lab  
**Version:** 1.0 (2026-02-19)

### Executive summary
Cloaked phishing kits often perform server-side access control before serving a malicious landing page. If the visitor does not match the intended victim profile, the kit returns benign content or redirects to a trusted site. This behavior causes traditional URL scanning and automated analysis to miss the real payload, producing a dangerous false sense of security.

This paper explains common cloaking gates, observable signals in enterprise telemetry, and practical detection and evidence-building approaches. It also includes a lightweight differential-fetch workflow (“CloakCheck”) to test URLs across multiple client profiles and measure response variance.

---

## 1. Threat model
### 1.1 What “cloaking” means in phishing
A cloaked kit serves *different* content depending on who is asking. The attacker’s goal is simple:
- **Victims** get the credential theft page (or payload).
- **Scanners, sandboxes, researchers** get something harmless.

### 1.2 Why server-side filtering matters
Client-side tricks (obfuscated JS, delayed loads) are annoying. Server-side filtering is worse because your analysis tooling can be rejected before it ever receives the malicious content.

---

## 2. Common gating signals used by kits
Kits frequently evaluate:

### 2.1 Geo targeting
- Country allowlists/denylists
- Region/locale constraints

### 2.2 Network targeting
- ISP/ASN allowlists
- Deny ranges for cloud providers, VPNs, and known scanners
- Reputation checks on IP or reverse DNS hints

### 2.3 Device and browser targeting
- Mobile-only flows (because corporate tooling often looks like desktop Chrome in a datacenter)
- User-Agent checks
- Accept-Language alignment
- Cookie presence (first click vs repeat visit)
- Referrer checks (did the user come from an email link?)

### 2.4 Time and campaign control
- Serve malicious content only during “business hours”
- Expire quickly once burned

---

## 3. Defender visibility: what you can actually measure
You typically don’t get a single “this was cloaked” log line. You infer it from patterns.

### 3.1 SWG / proxy telemetry
Look for:
- **Fast 30x redirects**, multi-hop chains
- **Inconsistent content** across clients (hash/length drift)
- **Rare domains** suddenly appearing for a small user set
- Redirects to benign destinations for some clients

### 3.2 DNS telemetry
- First-seen domains
- Burst lookups from a small cohort
- Short-lived domains tied to click timestamps

### 3.3 Email security telemetry
- Click events correlated with new domains
- Repeat clicks showing different behavior (kit “burn” patterns)

---

## 4. Differential testing workflow (CloakCheck)
### 4.1 Concept
Request the same URL multiple times while varying:
- User-Agent
- Accept-Language
- Referrer
- Optional custom headers

Capture:
- Redirect chain
- Response headers
- Body hash and length
- Title extraction

### 4.2 Interpreting results
Cloaking suspicion increases when:
- Final landing domain differs across profiles
- Hash drift is large and titles differ
- One profile sees “benign” (or empty) content while another sees structured login HTML
- Redirect hops include newly observed domains

### 4.3 False positives to consider
- CDN geo optimizations
- Consent pages varying by region
- Legit A/B tests
- Mobile rendering differences

The goal is not “convict on one signal.” The goal is evidence you can defend.

---

## 5. Detection starting points
This pack includes starter templates for:
- Splunk SPL
- Microsoft Sentinel (KQL)
- Elastic (KQL + ES|QL)
- Sigma (generic)

These focus on:
- Multi-hop redirects
- New domains
- Content variance
- “Campaign-ish” patterns (small cohort, sudden appearance)

---

## 6. Evidence packaging
Use the included evidence bundle template to produce an audit-friendly set of artifacts:
- Raw run outputs
- Comparison report
- Supporting SWG/DNS/email logs
- IOC list in a consistent schema (CSV/JSON/STIX)

Because “we think it was cloaked” is a vibe. **Evidence** is a fact.

---

## 7. Recommendations
1) **Stop relying on single-vantage URL scanning** as a pass/fail control.  
2) **Instrument redirect chains** in SWG and log them consistently.  
3) **Track first-seen domains** and alert on bursty, low-prevalence domains.  
4) **Use differential testing** for high-risk clicks and targeted campaigns.  
5) **Build a repeatable evidence workflow** so every investigation produces reusable detections.

---

## Appendix A — Files in this pack
- `scripts/zeid_data_differential_fetch.py`
- `scripts/zeid_data_compare_runs.py`
- `detections/*`
- `templates/*`
- `checklists/*`
- `data/*`

## Appendix B — IOC schema (minimum)
- `indicator_type` (domain|url|ip|hash|email|path|header|ua)
- `indicator_value`
- `first_seen`, `last_seen`
- `confidence` (low|medium|high)
- `source`
- `notes`
