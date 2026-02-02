# Zeid Data — Splunk Content (Free Drops)

This repo (or folder) is where Zeid Data publishes **Splunk-ready** security content: dashboards, detections, saved searches, lookups, and installable app artifacts you can ship into a SOC and defend in an audit.

No paywall. Just payload.

---

## What you’ll find here

Depending on the drop, content may include:

- **Dashboards**
  - Classic SimpleXML dashboards
  - Dashboard Studio JSON dashboards
- **Detections**
  - SPL searches (triage + hunting)
  - Correlation-style patterns (where applicable)
  - Tuning notes + false-positive guidance
- **Operational building blocks**
  - Macros (to make deployments portable)
  - Lookups (CSV) + field mappings
  - Knowledge objects (eventtypes, tags, calculated fields)
- **Packaging**
  - Standalone `.conf` snippets **or**
  - Full Splunk app folders that can be installed under `etc/apps/`

> Everything is designed to be: practical, reproducible, and explainable to engineers *and* auditors.

---

## Repo layout (typical)

Your structure may vary by drop, but most Splunk content follows a pattern like:

