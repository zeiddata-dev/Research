## Quick start (Splunk Enterprise)

1. **Clone** the repo.
2. If you’re installing an app:
   - Copy the app folder into:
     - `$SPLUNK_HOME/etc/apps/<app_name>/`
3. **Restart Splunk** (or reload configs where appropriate).
4. In Splunk Web:
   - Confirm the app appears
   - Review/enable the saved searches you want
   - Set required macros/lookups (if included)

---

## Quick start (Splunk Cloud)

Splunk Cloud installation varies by tenancy and app policy:

- If the drop is a **packaged app**, use your normal Splunk Cloud app installation process (or Cloud admin workflow).
- If the drop is **SPL + dashboards only**, you can often import dashboards and saved searches directly via Splunk Web / content management.

If a drop requires custom configs (props/transforms), check `docs/` for Cloud-safe alternatives.

---

## Configuration & portability

To keep deployments clean and portable, drops may rely on:

- **Macros** for index/sourcetype abstraction (so you don’t hardcode environment specifics)
- **Lookups** for enrichment and suppression
- **Field expectations** documented per detection/dashboard

If something doesn’t light up:
- Start by verifying required data models / sourcetypes / CIM alignment (if the content expects it)
- Confirm macros + lookups are present and readable
- Check time range + acceleration dependencies (if any)

---

## Evidence-first design

Each detection/dashboard should answer:

- **What signal is this using?**
- **Why does it matter?**
- **How do I validate it quickly?**
- **What’s the expected output?**
- **How do I tune it without breaking it?**

If it didn’t generate evidence, it didn’t happen.

---

## Safety & responsible use

This content is for **defensive security and audit readiness**.

- Only deploy/test on systems you own or are explicitly authorized to assess.
- Don’t treat example thresholds as “defaults” — tune to your environment.

---

## Contributing

PRs are welcome, especially for:

- Better SPL performance (fewer wildcards, smarter stats, data model usage when appropriate)
- Cleaner dashboards (actionable panels > vanity charts)
- Clearer tuning guidance + test data (sanitized)
- Portability improvements (macros, documented field requirements)

If you add new detections, include:
- A short `docs/` note explaining the signal + expected fields
- Tuning notes and common false-positive patterns

---

## Licensing

See the root `LICENSE` (or drop-specific license file if present).  
If you redistribute, keep attribution and don’t misrepresent origin.

---

## Trademarks

Splunk is a trademark of its respective owner. This project is not affiliated with or endorsed by Splunk.

---

## Where to follow updates

- New content is published as it’s built (because attackers don’t wait for your change control meeting)
