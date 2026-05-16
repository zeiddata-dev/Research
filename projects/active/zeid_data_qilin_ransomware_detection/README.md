<!-- ZEID DATA README HERO START -->
![Zeid Data projects banner](../../../assets/banners/readme/projects.png)

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../.."><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data - Copper Hang Back..
# comments: deposit ghost trace (copper)
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
