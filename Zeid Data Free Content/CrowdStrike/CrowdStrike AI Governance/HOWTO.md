# HOWTO — Install, Customize, and Use

## 1) Install the Package
- In Falcon LogScale, import this package as a **library** package.
- After install, the templates and saved searches will be available to use.

## 2) Create Dashboards from Templates
- Go to **Dashboards**
- Select **New dashboard**
- Choose **From template / package**
- Pick one of:
  - AI Governance — Overview
  - AI Governance — Tool Usage & Policy
  - AI Governance — Data Exposure Signals

## 3) Use Parameters (Filters)
These dashboards use simple wildcard parameters. Defaults are `*` (match everything).

Typical filters:
- `?host` → `ComputerName=?host`
- `?user` → `UserName=?user`
- `?domain_category` → `category=?domain_category`
- `?sanctioned` → `sanctioned=?sanctioned`

Wildcards supported (examples):
- `DESKTOP-*`
- `alice*`
- `*` (all)

## 4) Customize AI Allowlist Policy (Lookups)

### AI Domains
Edit: `data/ai_domains.csv`

Columns:
- `domain` — exact domain value you expect in logs (ex: `chat.openai.com`)
- `vendor` — OpenAI, Anthropic, Google, Microsoft, etc.
- `category` — chat, code, image, search, etc.
- `sanctioned` — `sanctioned` or `unsanctioned`
- `notes` — optional

Tip: Add the exact subdomains you see in your telemetry.

### AI Apps
Edit: `data/ai_apps.csv`

Columns:
- `image_file_name` — executable name (ex: `ChatGPT.exe`)
- `vendor`, `category`, `sanctioned`, `notes`

If your process field contains full paths, update the query to normalize it (e.g., extract basename) before matching.

### Data Movement Tools (Optional)
Edit: `data/data_movement_tools.csv`

Starter list of common export tools. The Data Exposure dashboard uses this to help you prioritize investigations.

## 5) Evidence Exports (Audit-Friendly)

Run the saved searches in `queries/` and export results:
- “Evidence — AI Domain Usage (Users/Hosts)”
- “Evidence — Unsanctioned AI Domain Usage”
- “Evidence — AI App Execution”

Export format suggestions:
- CSV for audit packet
- PDF screenshots of dashboard widgets for executive summaries

## 6) Tuning Checklist

If widgets are empty:
1. Run the “Data Presence Check” saved search.
2. Confirm event types exist (e.g., `DnsRequest`, `ProcessRollup2`).
3. Confirm field names (`DomainName`, `ImageFileName`, `ComputerName`, `UserName`).
4. Update dashboard queries to your schema.

## 7) Extensions (Optional)
- Add proxy/CASB/DLP sources for stronger “data exposure” signals.
- Create alerts from the evidence searches (unsanctioned usage thresholds, new domains, etc.).
