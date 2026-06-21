#!/usr/bin/env bash
# One-time bootstrap for the Zeid Data white paper pipeline.
# Vendors the OFL brand fonts, records checksums, installs tectonic if asked.
# Run from anywhere inside the repo. Idempotent.
# Usage: tools/scripts/zd_whitepaper_bootstrap.sh [--with-tectonic]

LOG=/tmp/zd_whitepaper_bootstrap.log
: > "$LOG"
red()  { if [ -t 2 ]; then printf '\033[31m%s\033[0m\n' "$*" >&2; else printf '%s\n' "$*" >&2; fi; }
say()  { printf '%s\n' "$*" | tee -a "$LOG"; }

ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$ROOT" ] || [ ! -f "$ROOT/templates/whitepaper/zd-whitepaper.tex" ]; then
  d=$(pwd)
  while [ "$d" != "/" ]; do
    [ -f "$d/templates/whitepaper/zd-whitepaper.tex" ] && { ROOT="$d"; break; }
    d=$(dirname "$d")
  done
fi
if [ -z "$ROOT" ] || [ ! -f "$ROOT/templates/whitepaper/zd-whitepaper.tex" ]; then
  red "FAIL: cannot find the pipeline root (templates/whitepaper/). Run from inside the kit or repo."
  echo exit_code=2; exit 2
fi
cd "$ROOT" || { red "FAIL: cannot cd to root"; echo exit_code=2; exit 2; }
say "root=$ROOT"

FD=templates/whitepaper/fonts
mkdir -p "$FD"

validate() { [ -f "$1" ] && [ "$(stat -c%s "$1" 2>/dev/null || echo 0)" -gt 20000 ]; }

# DM Serif Display Regular (static TTF, OFL)
if validate "$FD/DMSerifDisplay-Regular.ttf"; then
  say "OK   DMSerifDisplay-Regular.ttf already vendored"
else
  if curl -fsSL --retry 2 --max-time 90 \
    "https://github.com/google/fonts/raw/main/ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf" \
    -o "$FD/DMSerifDisplay-Regular.ttf" && validate "$FD/DMSerifDisplay-Regular.ttf"; then
    say "OK   DMSerifDisplay-Regular.ttf fetched"
  else
    red "FAIL: could not vendor DM Serif Display"; echo exit_code=5; exit 5
  fi
fi

# Inter Regular (instanced from the OFL variable font for a clean static weight)
if validate "$FD/Inter-Regular.ttf"; then
  say "OK   Inter-Regular.ttf already vendored"
else
  if ! python3 -c "import fontTools" >/dev/null 2>&1; then
    say "installing fonttools"
    pip install fonttools --break-system-packages -q >>"$LOG" 2>&1 || pip install --user fonttools -q >>"$LOG" 2>&1
  fi
  if curl -fsSL --retry 2 --max-time 120 \
    "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf" \
    -o /tmp/Inter-VF.ttf; then
    python3 - "$FD" <<'PY' >>"$LOG" 2>&1
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
fd=sys.argv[1]
f=TTFont('/tmp/Inter-VF.ttf')
instantiateVariableFont(f, {'wght':400, 'opsz':14}, inplace=True)
f.save(fd+'/Inter-Regular.ttf')
PY
    if validate "$FD/Inter-Regular.ttf"; then
      say "OK   Inter-Regular.ttf instanced (wght=400)"
    else
      red "FAIL: could not instance Inter"; echo exit_code=6; exit 6
    fi
  else
    red "FAIL: could not fetch Inter variable font"; echo exit_code=6; exit 6
  fi
fi

sha256sum "$FD"/*.ttf | tee "$FD/SHA256SUMS" >>"$LOG"
say "checksums written to $FD/SHA256SUMS"

if [ "$1" = "--with-tectonic" ]; then
  if command -v tectonic >/dev/null 2>&1; then
    say "OK   tectonic already installed: $(tectonic --version)"
  else
    say "installing tectonic"
    curl -fsSL --retry 2 --max-time 180 "https://drop-sh.fullyjustified.net" -o /tmp/install-tectonic.sh >>"$LOG" 2>&1
    DEST="${HOME}/.local/bin"; mkdir -p "$DEST"
    ( cd "$DEST" && sh /tmp/install-tectonic.sh ) >>"$LOG" 2>&1
    if [ -x "$DEST/tectonic" ]; then
      say "OK   tectonic installed to $DEST. Ensure $DEST is on PATH."
    else
      red "WARN: tectonic install did not land in $DEST. Install it manually."
    fi
  fi
fi

say "bootstrap complete"
echo exit_code=0
