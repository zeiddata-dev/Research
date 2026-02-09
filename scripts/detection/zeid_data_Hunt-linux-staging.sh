#!/usr/bin/env bash
# Hunt-linux-staging.sh
# Quick sweep for suspicious persistence/staging on Linux (cron/systemd/tmp + new executables).
# Usage: sudo ./Hunt-linux-staging.sh 7   # look back N days (default 7)

DAYS="${1:-7}"
SINCE="$(date -d "-$DAYS days" +%s)"

echo "[+] Looking back $DAYS day(s) (epoch >= $SINCE)"
echo

echo "[+] Recently modified cron entries:"
for p in /etc/crontab /etc/cron.*/* /var/spool/cron/*; do
  [ -e "$p" ] || continue
  m=$(stat -c %Y "$p" 2>/dev/null || echo 0)
  if [ "$m" -ge "$SINCE" ]; then
    echo "  - $p (modified: $(date -d "@$m"))"
  fi
done
echo

echo "[+] Recently modified systemd unit files:"
find /etc/systemd/system /lib/systemd/system -maxdepth 2 -type f 2>/dev/null | while read -r f; do
  m=$(stat -c %Y "$f" 2>/dev/null || echo 0)
  if [ "$m" -ge "$SINCE" ]; then
    echo "  - $f (modified: $(date -d "@$m"))"
  fi
done
echo

echo "[+] Suspicious executables in temp locations modified recently:"
find /tmp /var/tmp /dev/shm -type f -perm -111 2>/dev/null | while read -r f; do
  m=$(stat -c %Y "$f" 2>/dev/null || echo 0)
  if [ "$m" -ge "$SINCE" ]; then
    echo "  - $f (modified: $(date -d "@$m"))"
    file "$f" 2>/dev/null | sed 's/^/      /'
  fi
done
echo

echo "[+] Recent use of curl/wget in shell history files (best-effort):"
for h in /root/.bash_history /home/*/.bash_history; do
  [ -f "$h" ] || continue
  grep -E "curl|wget" "$h" 2>/dev/null | tail -n 5 | sed "s|^|  - $h: |"
done
