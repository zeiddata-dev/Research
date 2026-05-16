<!-- ZEID DATA README HERO START -->
<p align="center">
  <img src="../../../assets/banners/readme/projects_active_zeid_data_gap_check.svg" alt="Zeid Data Gap Check" width="100%">
</p>

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

# Zeid Data GapCheck (Air‑Gap Network Compliance Evidence Collector)

An offline-first CLI tool that collects **host-based network evidence** to help prove an environment is *air‑gapped* (or to identify where it isn’t). It produces a timestamped evidence bundle (raw command output + normalized JSON + human‑readable Markdown) suitable for audit attachments.

## Quick start
```bash
python gapcheck.py run --policy policy.sample.json --output ./evidence
```

## Authorized use only
Run this tool only on systems and networks you are authorized to assess.
