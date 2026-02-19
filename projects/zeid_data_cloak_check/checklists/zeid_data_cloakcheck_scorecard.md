# CloakCheck Suspicion Scorecard

Score each category 0–2 and total.

## 1) Redirect behavior drift (0–2)
- 0: Same chain across profiles
- 1: Minor differences (one hop differs) but same final domain
- 2: Different final domain and/or extra hops for some profiles

## 2) Content hash drift (0–2)
- 0: Same SHA256 across profiles
- 1: Minor drift with same title and similar length (likely benign variance)
- 2: Different title and/or large body differences (possible gating)

## 3) “New / rare domain” involvement (0–2)
- 0: All domains are known / established
- 1: One newly seen domain in the chain
- 2: Newly registered or rarely-seen domain is the final landing

## 4) Fast redirect timing (0–2)
- 0: No unusual timing
- 1: One quick 30x hop
- 2: Multi-hop 30x chain with short TTL behavior (campaign-y)

## 5) Targeting signals (0–2)
- 0: No obvious targeting markers
- 1: UA or language drives minor differences
- 2: Strong gating indicators (only “consumer mobile” gets the real page, etc.)

### Interpretation
- 0–3: Low (likely benign variance)
- 4–6: Medium (needs more context)
- 7–10: High (treat as cloaking until proven otherwise)

Attach the score to your evidence bundle. Leaders love numbers. Even when the numbers are brutally honest.
