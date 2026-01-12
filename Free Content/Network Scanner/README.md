███████╗███████╗██╗██████╗     ██████╗  █████╗ ████████╗ █████╗ 
╚══███╔╝██╔════╝██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
  ███╔╝ █████╗  ██║██║  ██║    ██║  ██║███████║   ██║   ███████║
 ███╔╝  ██╔══╝  ██║██║  ██║    ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗███████╗██║██████╔╝    ██████╔╝██║  ██║   ██║   ██║  ██║
╚══════╝╚══════╝╚═╝╚═════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝

# Zeid Data - Copper Hang Back...
# Network Inventory (No-Scan) — `network_inventory.py`

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
