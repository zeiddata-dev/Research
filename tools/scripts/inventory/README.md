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

# Zeid Data — Network Inventory Scripts (Research Labs)

This folder contains **10 small network-inventory scripts** written in different languages, intended for **authorized** environments only (your networks or systems you have explicit permission to assess).

## What these scripts do

Each script supports some combination of:
- **Passive inventory**: reads local ARP/neighbor cache (`ip neigh`, `arp -a`, `Get-NetNeighbor`) to list recently observed IP/MAC pairs.
- **Optional active discovery (opt-in)**: basic **ICMP ping sweep** across a provided subnet to identify responders and help populate neighbor tables.
- **Optional reverse DNS (best-effort)**: resolves hostnames where possible.

No exploitation, no stealth, no credential collection.

## Included scripts

1. `zeid_data_inventory_python.py` (Python) — JSONL/CSV
2. `zeid_data_inventory_powershell.ps1` (PowerShell) — CSV/JSONL
3. `zeid_data_inventory_bash.sh` (Bash) — CSV
4. `zeid_data_inventory_go.go` (Go) — JSONL
5. `zeid_data_inventory_rust.rs` (Rust) — CSV
6. `zeid_data_inventory_node.js` (Node.js) — JSONL
7. `zeid_data_inventory_ruby.rb` (Ruby) — CSV
8. `zeid_data_inventory_perl.pl` (Perl) — CSV
9. `zeid_data_inventory_csharp.cs` (C#) — JSON
10. `zeid_data_inventory_java.java` (Java) — JSONL

## Quick usage

Python:
- `python zeid_data_inventory_python.py --out inventory.jsonl --format jsonl`
- `python zeid_data_inventory_python.py --subnet 192.168.1.0/24 --active --dns --out inventory.csv --format csv`

PowerShell:
- `./zeid_data_inventory_powershell.ps1 -OutFile inventory.jsonl -Format jsonl`
- `./zeid_data_inventory_powershell.ps1 -Subnet 192.168.1.0/24 -Active -DNS -OutFile inventory.csv -Format csv`

Bash:
- `sudo ./zeid_data_inventory_bash.sh --out inventory.csv`
- `sudo ./zeid_data_inventory_bash.sh --subnet 192.168.1.0/24 --active --out inventory.csv`

Go:
- `go run zeid_data_inventory_go.go -out inventory.jsonl`
- `go run zeid_data_inventory_go.go -subnet 192.168.1.0/24 -active -dns -out inventory.jsonl`

Rust:
- `rustc zeid_data_inventory_rust.rs && ./zeid_data_inventory_rust --out inventory.csv`
- `./zeid_data_inventory_rust --subnet 192.168.1.0/24 --active --out inventory.csv`

Node:
- `node zeid_data_inventory_node.js --out inventory.jsonl`
- `node zeid_data_inventory_node.js --subnet 192.168.1.0/24 --active --dns --out inventory.jsonl`

Ruby:
- `ruby zeid_data_inventory_ruby.rb --out inventory.csv`
- `ruby zeid_data_inventory_ruby.rb --subnet 192.168.1.0/24 --active --out inventory.csv`

Perl:
- `perl zeid_data_inventory_perl.pl --out inventory.csv`
- `perl zeid_data_inventory_perl.pl --subnet 192.168.1.0/24 --active --out inventory.csv`

C# (dotnet):
- `dotnet new console -n ZeidDataInv`
- Replace `Program.cs` with the contents of `zeid_data_inventory_csharp.cs`
- `dotnet run -- --subnet 192.168.1.0/24 --active --out inventory.json`

Java:
- `javac zeid_data_inventory_java.java && java zeid_data_inventory_java --out inventory.jsonl`
- `java zeid_data_inventory_java --subnet 192.168.1.0/24 --active --dns --out inventory.jsonl`
