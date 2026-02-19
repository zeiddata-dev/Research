# Zeid Data – Research and Detection Engineering

## Security Policy

We take security seriously. Not “seriously” like a checkbox on a slide deck. Seriously like: if you found a vuln, we want to fix it before it becomes a live demo on someone’s blog.

If you believe you’ve found a security issue in this repo, report it responsibly so we can handle it quickly and safely.

## Supported Versions

Security fixes are applied to:

* The default branch (usually `main`)
* The latest published release (if we’re doing releases)

Older commits, forks, screenshots of forks, and that one pinned copy living in a dark corner of the internet may not get fixes. That’s just physics.

## Reporting a Vulnerability

**Please do not open a public GitHub Issue for security vulnerabilities.**
Yes, even if you title it “URGENT VULN!!!” with twelve exclamation points. That makes it worse.

Instead, email:

* **[security@zeiddata.com](mailto:security@zeiddata.com)**

Include as much as you can:

* A clear description of the issue and impact (what breaks, who cries, what burns)
* Reproduction steps or a PoC (safe, minimal, and not a ransomware speedrun)
* Affected path(s) file(s) module(s)
* Any suggested fix or mitigation (if you’ve got one, we love you)
* Your contact info (and how you want to be credited, if at all)

If the issue involves **credentials, tokens, private keys, customer data, or sensitive logs**, say that clearly and **do not** paste real secrets. Use redacted examples.
If you leak a key into an email thread, congrats, you created a second incident.

## What to Expect

We aim to:

* Acknowledge receipt within **3 business days** (we saw it, we’re on it, we’re not ignoring you)
* Provide an initial assessment and next steps within **7 business days**
* Coordinate disclosure timelines with you if a patch is needed

Timelines vary depending on severity and complexity. Sometimes it’s one line. Sometimes it’s archaeology.

## Coordinated Disclosure

We support coordinated disclosure. We’ll work with you on:

* Severity confirmation (no, “it feels spicy” isn’t a CVSS score)
* Patch development and release planning
* A reasonable public disclosure date

If you plan to publish details, please give us a chance to patch first.
Surprise drops are for albums, not vulnerabilities.

## Scope

This policy covers:

* Code, scripts, and detections in this repository
* Documentation and configuration examples in this repository

Out of scope (unless explicitly stated otherwise):

* Vulnerabilities in third party dependencies (please report upstream too)
* Issues caused by unsafe configuration or running tools outside documented use
  (If you run it as root on prod and it explodes, that’s a lifestyle choice.)

## Safe Harbor

We will not pursue legal action against researchers who:

* Make a good faith effort to follow this policy
* Avoid privacy violations, data destruction, and service disruption
* Do not exploit the vulnerability beyond what’s necessary to demonstrate it

In short: be cool, don’t break stuff, don’t touch data you don’t need.

## Security Notes for Contributors

* Never commit secrets (API keys, tokens, passwords, private keys).
* Prefer `.env` files locally and add them to `.gitignore`.
* If you accidentally commit a secret, rotate it immediately and notify us at **[security@zeiddata.com](mailto:security@zeiddata.com)**.
  “I’ll fix it later” is how incident timelines begin.

Thanks for helping keep Zeid Data tooling and research safer for everyone.
