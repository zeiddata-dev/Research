███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║
╚══════╝╚══════╝╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
# Zeid Data - Copper Hang Back...
# Qilin (and optional Akira) Ransomware Triage Scanner — Windows

A **quick, read-only file-system triage** script for Windows that searches for **common ransomware artifacts** associated with **Qilin** (and optionally **Akira**) such as:
- Encrypted file extensions (e.g., `*.qilin`, optionally `*.akira`)   
- Ransom note filename patterns (e.g., `README-RECOVER-*.txt`)   

> ⚠️ **Important:** This script is **not a guarantee of safety** and it is **not a replacement** for EDR/AV or incident response. It’s meant to help you quickly identify **high-signal indicators** during initial triage.

---

## What this script does

✅ Scans one or more root folders (defaults to `C:\Users` and `C:\ProgramData`)  
✅ Looks for:
- **Qilin** encrypted extension: `.qilin`   
- **Qilin** ransom note patterns: `README-RECOVER-*.txt`   
✅ Optionally looks for **Akira** artifacts:
- `.akira`
- `akira_readme.txt`, `fn.txt`   
✅ Outputs a **JSON report** + prints a short console summary

---

## What this script does *not* do

❌ It does not detect memory-only/fileless activity  
❌ It does not reliably identify the ransomware executable (names/hashes change)  
❌ It does not perform remediation, decryption, or recovery  
❌ It does not replace incident response best practices

---

## Requirements

- Windows 10/11
- Python 3.10+ recommended (3.8+ usually works)

Check your Python version:

```powershell
python --version
