# HOWTO: CloakCheck (Cloaked Phishing Differential Fetch)

## Goal
Prove (or disprove) whether a URL behaves differently based on visitor profile — before you tell leadership “the scanner said it was fine.”

## Step 0 — Decide your “profiles”
Cloaked kits commonly gate by:
- Geography (country / region)
- ASN / ISP (exclude datacenters, VPNs, known scanners)
- Device type (mobile vs desktop)
- Browser fingerprints (UA, headers, language)
- Time windows, cookies, referrers

CloakCheck approximates this by varying:
- User-Agent
- Accept-Language
- Referrer
- Optional custom headers
- Optional “simulate mobile” (UA + viewport-ish hints)

## Step 1 — Run a single URL
```bash
python scripts/zeid_data_differential_fetch.py --url "https://..." --out runs
```

Outputs per run:
- redirect chain (status codes + locations)
- response headers
- body hash (SHA256)
- content length
- HTML title (if available)
- a small “body preview” snippet for triage

## Step 2 — Run a batch list
Put URLs in `scripts/zeid_data_urls_sample.txt` (one per line) and run:
```bash
python scripts/zeid_data_differential_fetch.py --infile scripts/zeid_data_urls_sample.txt --out runs
```

## Step 3 — Compare and score
```bash
python scripts/zeid_data_compare_runs.py --runs runs --report runs/zeid_data_comparison_report.md
```
This generates:
- per-URL variance table (redirect drift, hash drift, length drift)
- a simple “cloak suspicion score” (see scorecard)

## Step 4 — Turn it into evidence
Use `checklists/zeid_data_evidence_bundle_template.md` to package:
- raw run JSON
- comparison report
- screenshots (if you captured any via your proxy/browser tooling)
- timeline (first seen, users impacted, blocks applied)

## Step 5 — Deploy detections
Pick your stack:
- Splunk: `detections/zeid_data_splunk_cloakcheck.spl`
- Sentinel: `detections/zeid_data_sentinel_cloakcheck.kql`
- Elastic: `detections/zeid_data_elastic_kql_cloakcheck.txt` and `detections/zeid_data_elastic_esql_cloakcheck.esql`
- Sigma (generic): `detections/zeid_data_sigma_cloaked_phishing.yml`

### Notes on telemetry
Cloaking detection works best when you have:
- Secure Web Gateway / proxy logs with redirect info
- DNS logs for newly seen domains
- EDR browser telemetry (optional)
- Email security logs (who clicked, when)

## Common false positives
- Legit A/B testing
- Geo-based CDN behavior
- Consent pages varying by region
- Mobile optimized landing pages

That’s why CloakCheck focuses on *patterns* (multi-hop redirects + new domains + fast behavior changes), not a single indicator.

## If you want screenshots / DOM snapshots
CloakCheck ships a lightweight HTTP collector. If you need “real browser” rendering, use your lab tooling (Playwright / Selenium) and attach captures as evidence.
