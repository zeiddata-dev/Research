# Evidence Bundle Template: Cloaked Phishing / Cloaking Suspected

## Summary
- Incident name:
- Date range:
- Report owner:
- Systems affected:
- Users impacted:
- Current status:

## What happened
Short narrative: click → redirect chain → final landing differences.

## Key findings
- Variance observed across profiles:
- Redirect drift:
- Content hash drift:
- Newly observed domains:

## Artifacts included
- `runs/` raw CloakCheck JSON outputs
- `runs/zeid_data_comparison_report.md`
- Proxy/SWG logs (export)
- DNS logs (export)
- Email security click logs (export)
- Screenshots / HAR files (if collected)

## Timeline
- First seen:
- First click:
- Blocks applied:
- Containment complete:
- Lessons learned:

## IOCs
Provide as CSV and/or STIX using `templates/` schemas.

## Mitigations applied
- Domain blocks:
- URL/path blocks:
- SWG policy changes:
- User comms:
- Retro-hunt queries executed:

## Notes / caveats
- Potential false positive causes (A/B tests, CDN behavior):
- Gaps in telemetry:
