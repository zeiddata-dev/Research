<!-- ZEID DATA README HERO START -->
![Zeid Data scripts banner](../../../assets/banners/readme/scripts.png)

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![automation](https://img.shields.io/badge/automation-2EA043?style=flat-square) ![scripts](https://img.shields.io/badge/scripts-334155?style=flat-square) ![cli-tools](https://img.shields.io/badge/cli%20tools-334155?style=flat-square) ![tooling](https://img.shields.io/badge/tooling-334155?style=flat-square) ![validators](https://img.shields.io/badge/validators-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data — Automation Scripts 🤖⚙️  
_Where repetitive work goes to get replaced by a command that you’ll forget the flags for by next week._

Welcome to the **Zeid Data Automation Scripts** directory: a rotating collection of utilities that do the boring stuff reliably, repeatedly, and without needing a “quick screen share” every time the same task comes back around.

These scripts are for operators, engineers, and anyone who has ever thought:
> “There has to be a way to automate this.”  
…and then immediately regretted having that thought because now it’s your job.

---

## What this directory contains
A wide variety of scripts across common operational domains, including (but not limited to):

- **System administration**: users, services, scheduled tasks, configs, package sanity  
- **Network operations**: inventory, reachability checks, port checks, DNS verification, route hints  
- **Security & compliance**: baseline validation, artifact collection, evidence generation, drift checks  
- **Cloud/platform chores**: API-driven collection and control validation (when the API is behaving)  
- **Data handling**: parsing, normalization, report generation, “turn logs into something defensible”

If it’s repetitive, error-prone, or expensive to do by hand—welcome home.

---

## Goals (aka “why this exists”)
These scripts aim to be:

- **Deterministic**: same inputs → same outputs (no “it depends” astrology)  
- **Automation-friendly**: runnable in CI/CD, schedulers, and non-interactive environments  
- **Auditable**: produce artifacts you can attach to tickets, incidents, or compliance evidence  
- **Explicit**: clear exit codes, clear errors, clear outputs (no vague “maybe” energy)  
- **Lean**: minimal dependencies and fewer “install 12 things” pre-flight rituals  

---

## Typical structure
Most scripts follow a predictable layout so you’re not spelunking in mystery folders:



automation/
tools/scripts/
<script_name>/
README.md # what it does, what it needs, what it outputs
HOWTO.md # copy/paste examples + operational guidance
src/ # the script(s)
examples/ # sample inputs/configs
output/ # generated artifacts (usually gitignored)
tests/ # if we were feeling responsible


Some scripts may be single-file utilities (because not every tool needs a novel written about it… even if we still write one).

---

## How to run scripts without creating a new incident
1. **Read the script’s `README.md`**  
   It tells you what the script does, what it refuses to do, and what it will absolutely do if you point it at the wrong thing.

2. **Follow `HOWTO.md`**  
   Usually includes:
   - prerequisites
   - example commands
   - expected outputs
   - troubleshooting notes
   - “don’t do this in prod unless you mean it” warnings

3. **Run in a safe place first**  
   If you can test it in a lab or staging environment, do that.  
   If you can’t… at least pretend you considered it.

---

## Outputs & artifacts
Many scripts generate artifacts such as:

- JSON / CSV summaries
- logs (`.log`)
- timestamped “evidence bundles”
- reports intended for tickets and runbooks

Common output behaviors:
- **Timestamped folders** (because overwriting evidence is a fun way to lose arguments)
- **Machine-readable formats** (because screenshots are not telemetry)
- **Exit codes that mean something** (because “success” shouldn’t be implied)

If a script prints nothing, it’s either:
- being polite, or  
- failing somewhere you didn’t look yet.  
Check the output directory and logs before declaring it “broken.”

---

## Safety and responsibility
Automation is a power tool. Power tools do not negotiate.

- Use **least privilege** credentials.
- Don’t run destructive actions in production unless you’ve read the code or trust the script’s behavior.
- If a script supports a `--dry-run` mode, use it first.
- If you don’t understand a flag, do not treat it like a “mystery button.”  
  Mystery buttons belong in video games, not infrastructure.

---

## Conventions you’ll see here
To keep things consistent and predictable:

- **Sane defaults** when possible
- **Config over hardcoding**
- **Structured logs** (often JSON lines when feasible)
- **Clear error messages** (no interpretive dance required)
- **Evidence-first mindset**: outputs are meant to be saved, reviewed, and attached to real workflows

We like receipts. Especially the kind auditors can parse without calling you.

---

## Contributing (yes, you can add to the pile)
If you add or modify a script:

- Include a `README.md` and `HOWTO.md`
- Document inputs, outputs, and failure modes
- Keep the script deterministic and automation-safe
- Avoid dependency explosions for trivial tasks
- Add at least one working example invocation

Bonus points if your script produces clean artifacts that can be attached to a ticket with zero explanation.
Because if it didn’t generate evidence, it didn’t happen.

---

## Disclaimer
These scripts are provided as-is.

They are not sentient.  
They do not “know what you meant.”  
They will do exactly what you told them to do, with the enthusiasm of a machine that has never been held accountable for consequences.

So, double-check your targets, verify your flags, and try not to turn your environment into an accidental case study.

---

## Quick start
1) Pick a script under `automation/tools/scripts/<script_name>/`  
2) Open `HOWTO.md`  
3) Copy the example command  
4) Run it  
5) Enjoy reclaiming a few minutes of your life from the GUI
