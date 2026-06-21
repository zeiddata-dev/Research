#!/usr/bin/env bash
# Build a Zeid Data white paper to PDF. Run from anywhere inside the repo.
# Usage: tools/scripts/zd_whitepaper_build.sh research/<section>/<slug>
#    or: tools/scripts/zd_whitepaper_build.sh research/<section>/<slug>/paper.tex
# Resolves the repo root itself, detects the toolchain, fails loud if none.

LOG=/tmp/zd_whitepaper_build.log
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
cd "$ROOT" || { red "FAIL: cannot cd to root $ROOT"; echo exit_code=2; exit 2; }
say "root=$ROOT"

ARG="$1"
if [ -z "$ARG" ]; then red "FAIL: pass the paper dir or paper.tex path"; echo exit_code=2; exit 2; fi
case "$ARG" in
  *.tex) TEX="$ARG" ;;
  *)     TEX="${ARG%/}/paper.tex" ;;
esac
if [ ! -f "$TEX" ]; then red "FAIL: $TEX not found"; echo exit_code=2; exit 2; fi
OUTDIR=$(dirname "$TEX")
say "paper=$TEX"
say "outdir=$OUTDIR"

if [ ! -f templates/whitepaper/fonts/Inter-Regular.ttf ] || [ ! -f templates/whitepaper/fonts/DMSerifDisplay-Regular.ttf ]; then
  red "FAIL: brand fonts missing. Run tools/scripts/zd_whitepaper_bootstrap.sh first."
  echo exit_code=3; exit 3
fi

if command -v tectonic >/dev/null 2>&1; then
  TOOL=tectonic
  say "DECISION: toolchain=tectonic"
  tectonic --chatter minimal --outdir "$OUTDIR" "$TEX" >>"$LOG" 2>&1; rc=$?
elif command -v latexmk >/dev/null 2>&1; then
  TOOL=latexmk
  say "DECISION: toolchain=latexmk"
  latexmk -xelatex -interaction=nonstopmode -outdir="$OUTDIR" "$TEX" >>"$LOG" 2>&1; rc=$?
elif command -v xelatex >/dev/null 2>&1; then
  TOOL=xelatex
  say "DECISION: toolchain=xelatex"
  ( cd "$OUTDIR" && xelatex -interaction=nonstopmode "$(basename "$TEX")" && xelatex -interaction=nonstopmode "$(basename "$TEX")" ) >>"$LOG" 2>&1; rc=$?
else
  red "DECISION: toolchain=MISSING"
  red "FAIL: no LaTeX engine found. Install tectonic:"
  red "  curl -fsSL https://drop-sh.fullyjustified.net | sh   then move ./tectonic into PATH"
  echo exit_code=4; exit 4
fi

PDF="$OUTDIR/$(basename "${TEX%.tex}").pdf"
if [ "$rc" -eq 0 ] && [ -f "$PDF" ]; then
  pages=$(command -v pdfinfo >/dev/null 2>&1 && pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/{print $2}')
  say "BUILD OK toolchain=$TOOL pdf=$PDF pages=${pages:-unknown}"
  echo exit_code=0
else
  red "BUILD FAILED toolchain=$TOOL rc=$rc"
  red "last errors:"; grep -i "error" "$LOG" | tail -5 >&2
  echo exit_code=1; exit 1
fi
