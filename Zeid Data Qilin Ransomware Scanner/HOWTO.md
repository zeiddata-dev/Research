Zeid Data - Copper Hang Back...
# HOWTO.md — Qilin / Akira Windows Triage Scanner
This is a **read-only** triage helper that scans your Windows file system for **high-signal ransomware artifacts** commonly associated with:
- **Qilin** (`*.qilin`, `README-RECOVER-*.txt`)
- **Akira** *(optional)* (`*.akira`, `akira_readme.txt`, `fn.txt`)

It generates a **JSON report** you can review yourself or hand to an IR/EDR team.

---

## 1) Before you run it (recommended)

If you suspect active ransomware:
1. **Disconnect the device from the network**
   - Turn off Wi-Fi / unplug Ethernet
2. **Don’t reboot repeatedly**
3. Close apps and save what you can

> This script does not remove anything. It only looks for indicators.

---

## 2) Get the script onto the machine

### Option A — From your GitHub repo
```powershell
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>
Option B — Copy the script manually
Copy qilin_triage_scan.py onto the machine (USB, secure share, etc.).

3) Verify Python is installed
Open PowerShell and run:

powershell
Copy code
python --version
If you don’t have Python, install Python 3 from the official source and re-run the command.

4) Run the scan
Quick scan (defaults)
Scans:

C:\Users

C:\ProgramData

powershell
Copy code
python .\qilin_triage_scan.py
Recommended: recent activity + stronger signal
Only looks at files modified in the last 72 hours, checks Akira too, and samples suspected note contents for generic keywords:

powershell
Copy code
python .\qilin_triage_scan.py --since-hours 72 --include-akira --sample-note-contents
Scan additional drives / folders
powershell
Copy code
python .\qilin_triage_scan.py --paths C:\Users C:\ProgramData D:\ E:\ --since-hours 168 --include-akira
Save the report with a custom name
powershell
Copy code
python .\qilin_triage_scan.py --out zeiddata_ransom_triage.json
5) Where the report goes
The script writes a JSON file in the current folder, like:

qilin_scan_report_YYYYMMDD_HHMMSS.json

You’ll also see a console summary with hit counts.

6) How to interpret results
High-confidence indicators
Many *.qilin files across user folders

Multiple README-RECOVER-*.txt files spread across directories

A burst of hits within a recent time window (--since-hours)

Why there can be false positives
A single text file matching the note pattern could be unrelated

Ransomware families change filenames and extensions over time

Permission errors are normal in protected Windows directories

7) Next steps if you get hits
If you see many hits across multiple folders:

Keep the machine offline

Run a full AV/EDR scan (Microsoft Defender Offline scan is a good baseline)

Preserve evidence (don’t wipe immediately)

Begin scoping:

Are other machines showing the same artifacts?

Are there shared drives impacted?

What’s the earliest modified time in findings?

8) Tips for faster scans
Use --since-hours to reduce noise and time

Focus on likely impact areas first:

C:\Users

C:\ProgramData

Any mapped drives or file shares (D:\, E:\, etc.)

Run PowerShell as Administrator to reduce permission errors

9) Full command reference
Option	What it does
--paths <list>	Root paths to scan
--since-hours N	Only consider files modified in last N hours
--include-akira	Also scan for Akira artifacts
--sample-note-contents	Reads up to 64KB of suspected notes for generic keywords
--exclude <names>	Directory names to skip (prunes everywhere)
--max-findings N	Stop after N hits to keep reports manageable
--out <file>	Output report filename

Example:

powershell
Copy code
python .\qilin_triage_scan.py --paths C:\Users D:\ --since-hours 48 --include-akira --sample-note-con
