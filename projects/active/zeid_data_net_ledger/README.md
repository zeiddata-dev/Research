<!-- ZEID DATA README HERO START -->
<p align="center">
  <img src="../../../assets/banners/readme/projects_active_zeid_data_net_ledger.svg" alt="Zeid Data Net Ledger" width="100%">
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

# Zeid Data - Copper Hang Back...
# comments: deposit ghost trace (copper)
# Zeid Data ProofScan — `network_inventory.py`

A **safe, educational** Python script that lists devices your computer already knows about from its **ARP / neighbor table**.  
✅ **No active scanning** • ✅ **Offline-friendly** • ✅ Works on **Windows / macOS / Linux**

> **Important:** This script does **not** probe or scan your network. It only reads your system’s existing ARP/neighbor cache, which is populated when your computer communicates with devices on your local network.

---

## What it does

- Reads your OS neighbor table:
  - **Windows:** `arp -a`
  - **macOS:** `arp -a`
  - **Linux:** `ip neigh` (preferred) or `arp -a`
- Extracts **IP address**, **MAC address**, and (when available) **interface** and **state**
- Prints a clean table to your terminal

---

## Requirements

- Python **3.8+** (recommended)
- No external dependencies (standard library only)

---

## Installation

1. Save the script as:

   `network_inventory.py`

2. (Optional) Put it in a folder, e.g.:

   ```bash
   mkdir network-inventory
   cd network-inventory
