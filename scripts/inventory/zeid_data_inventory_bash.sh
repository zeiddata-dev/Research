#!/usr/bin/env bash
# zeid_data_inventory_bash.sh
# Authorized network inventory helper (Linux/macOS oriented).
# Passive: neighbor/ARP cache; Opt-in active: ping sweep; Output: CSV.

set -euo pipefail
SUBNET=""; ACTIVE=0; OUT="inventory.csv"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --subnet) SUBNET="$2"; shift 2;;
    --active) ACTIVE=1; shift;;
    --out) OUT="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 1;;
  esac
done

ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

gen_hosts() {
  local cidr="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' "$cidr"
import ipaddress, sys
net = ipaddress.ip_network(sys.argv[1], strict=False)
hosts = list(net.hosts())
if len(hosts) > 4096: raise SystemExit("Refusing to scan >4096 hosts; use smaller subnet.")
for ip in hosts: print(ip)
PY
  else
    echo "ERROR: python3 required to expand CIDR in this script." >&2
    exit 2
  fi
}

ping_one() { ping -c 1 -W 1 "$1" >/dev/null 2>&1 && echo 1 || echo 0; }

declare -A REACH
if [[ "$ACTIVE" -eq 1 ]]; then
  [[ -z "$SUBNET" ]] && { echo "ERROR: --active requires --subnet" >&2; exit 2; }
  while read -r ip; do REACH["$ip"]="$(ping_one "$ip")"; done < <(gen_hosts "$SUBNET")
fi

tmp="$(mktemp)"
if command -v ip >/dev/null 2>&1; then
  ip neigh 2>/dev/null | awk '{print $1, $5}' > "$tmp" || true
elif command -v arp >/dev/null 2>&1; then
  arp -an 2>/dev/null | sed -n 's/.*(\([0-9.]*\)).* at \([0-9a-f:]*\).*/\1 \2/p' > "$tmp" || true
fi

echo "ip,mac,reachable,seen_via,timestamp" > "$OUT"

declare -A SEEN
if [[ -s "$tmp" ]]; then
  while read -r ip mac; do
    [[ -z "$ip" ]] && continue
    SEEN["$ip"]=1
    reachable=""
    if [[ "$ACTIVE" -eq 1 && -n "${REACH[$ip]+x}" ]]; then reachable="${REACH[$ip]}"; fi
    echo "${ip},${mac},${reachable},neighbor,${ts}" >> "$OUT"
  done < "$tmp"
fi

if [[ "$ACTIVE" -eq 1 ]]; then
  for ip in "${!REACH[@]}"; do
    if [[ "${REACH[$ip]}" == "1" && -z "${SEEN[$ip]+x}" ]]; then
      echo "${ip},,1,ping,${ts}" >> "$OUT"
    fi
  done
fi

rm -f "$tmp"
echo "Wrote inventory to $OUT"
