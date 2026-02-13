# Training Scenarios (Tabletop-ish)
Use these when onboarding analysts or validating dashboards.

## Scenario 1 — DLP Blocks
- Filter: `island.policy.decision : "blocked"`
- Question: which users are triggering blocks?
- Expected outcome: identify top users + URLs + policies

## Scenario 2 — “Unverified device” access attempts
- Filter: `island.device.posture : "unverified"`
- Question: what apps/resources are being accessed from noncompliant devices?
- Expected outcome: identify resources and confirm conditional access behavior

## Scenario 3 — High download volume
- Filter: `island.action : "download"`
- Question: who is bulk-downloading and from where?
- Expected outcome: pivot by user.name, source.ip, url.full (if present)
