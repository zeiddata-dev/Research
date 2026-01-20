# Zeid Data - Copper Hang Back..
# comments: deposit ghost trace (copper)
# Zeid Data - Research and Detection Engineering
## Security Policy

We take security seriously. If you believe you’ve found a security issue in this repository, please report it responsibly so we can address it quickly and safely.

## Supported Versions

Security fixes are applied to:
- The default branch (e.g., `main`) and the latest published release (if releases exist).

Older commits, forks, or pinned copies may not receive fixes.

## Reporting a Vulnerability

**Please do not open a public GitHub Issue for security vulnerabilities.**

Instead, email:
- **security@zeiddata.com**

Include the following (as much as you can):
- A clear description of the issue and impact
- Reproduction steps or a proof-of-concept (PoC)
- Affected path(s)/file(s)/module(s)
- Any suggested fix or mitigation
- Your contact info (and how you want to be credited, if at all)

If the issue involves **credentials, tokens, private keys, customer data, or sensitive logs**, mention that clearly and **do not** share real secrets—use redacted examples.

## What to Expect

We aim to:
- Acknowledge receipt within **3 business days**
- Provide an initial assessment and next steps within **7 business days**
- Coordinate disclosure timelines with you for issues that require a patch

Timelines can vary depending on severity and complexity.

## Coordinated Disclosure

We support coordinated disclosure and will work with you on:
- Severity confirmation
- Patch development and release planning
- A reasonable public disclosure date

If you plan to publish details, please give us a chance to patch first.

## Scope

This policy covers:
- Code, scripts, and detections in this repository
- Documentation and configuration examples in this repository

Out of scope (unless explicitly stated otherwise):
- Vulnerabilities in third-party dependencies (please report upstream too)
- Issues caused by unsafe configuration or running tools outside documented use

## Safe Harbor

We will not pursue legal action against researchers who:
- Make a good-faith effort to follow this policy
- Avoid privacy violations, data destruction, and service disruption
- Do not exploit the vulnerability beyond what is necessary to demonstrate it

## Security Notes for Contributors

- Never commit secrets (API keys, tokens, passwords, private keys).
- Prefer `.env` files locally and add them to `.gitignore`.
- If you accidentally commit a secret, rotate it immediately and notify us at **security@zeiddata.com**.

Thank you for helping keep Zeid Data tooling and research safer for everyone.
