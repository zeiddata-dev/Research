#!/usr/bin/env bash
# Ship one white paper end to end from inside the repo:
# build PDF, cut branch, commit, push, open PR into main. One command.
# Usage: tools/scripts/zd_whitepaper_ship.sh research/<section>/<slug>
# Requires: git, gh (authenticated), and the build toolchain.

LOG=/tmp/zd_whitepaper_ship.log
: > "$LOG"
red() { if [ -t 2 ]; then printf '\033[31m%s\033[0m\n' "$*" >&2; else printf '%s\n' "$*" >&2; fi; }
say() { printf '%s\n' "$*" | tee -a "$LOG"; }

ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -z "$ROOT" ] && { red "FAIL: not inside a git repo"; echo exit_code=2; exit 2; }
cd "$ROOT" || { red "FAIL: cannot cd to repo root"; echo exit_code=2; exit 2; }

PDIR="${1%/}"
[ -z "$PDIR" ] && { red "FAIL: pass the paper dir, e.g. research/<section>/<slug>"; echo exit_code=2; exit 2; }
[ -f "$PDIR/paper.tex" ] || { red "FAIL: $PDIR/paper.tex not found"; echo exit_code=2; exit 2; }
[ -f "$PDIR/meta.yml" ]  || { red "FAIL: $PDIR/meta.yml not found"; echo exit_code=2; exit 2; }

command -v gh >/dev/null 2>&1 || { red "FAIL: gh not installed. https://cli.github.com"; echo exit_code=3; exit 3; }
gh auth status >/dev/null 2>&1 || { red "FAIL: gh not authenticated. Run: gh auth login"; echo exit_code=3; exit 3; }

# Pull fields with python (lab machine has python3). No external yaml dep.
read_meta() { python3 - "$PDIR/meta.yml" "$1" <<'PY'
import sys,re
f,key=sys.argv[1],sys.argv[2]
for line in open(f):
    m=re.match(r'\s*'+re.escape(key)+r'\s*:\s*"?(.*?)"?\s*$',line)
    if m: print(m.group(1)); break
PY
}
TITLE=$(read_meta title); SLUG=$(read_meta slug); SECTION=$(read_meta section); DATE=$(read_meta date)
[ -z "$SLUG" ] && SLUG=$(basename "$PDIR")
[ -z "$DATE" ] && DATE=$(date +%F)
[ -z "$TITLE" ] && TITLE="$SLUG"
BRANCH="paper/${DATE}-${SLUG}"
say "title=$TITLE"; say "section=$SECTION"; say "branch=$BRANCH"

# fonts + build
if [ ! -f templates/whitepaper/fonts/Inter-Regular.ttf ] || [ ! -f templates/whitepaper/fonts/DMSerifDisplay-Regular.ttf ]; then
  say "vendoring fonts"; bash tools/scripts/zd_whitepaper_bootstrap.sh >>"$LOG" 2>&1
fi
say "building"
bash tools/scripts/zd_whitepaper_build.sh "$PDIR" >>"$LOG" 2>&1
[ -f "$PDIR/paper.pdf" ] || { red "FAIL: build produced no PDF. See $LOG"; grep -i error "$LOG" | tail -5 >&2; echo exit_code=4; exit 4; }
PAGES=$(command -v pdfinfo >/dev/null 2>&1 && pdfinfo "$PDIR/paper.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')

# clean working tree check, then branch
if ! git diff --quiet || ! git diff --cached --quiet; then
  red "FAIL: working tree dirty. Commit or stash first."; echo exit_code=5; exit 5
fi
git fetch origin --quiet
git checkout -b "$BRANCH" origin/main >>"$LOG" 2>&1 || git checkout -b "$BRANCH" >>"$LOG" 2>&1

git add "$PDIR" templates/whitepaper tools docs research/.gitignore 2>/dev/null
git commit -q -m "research(${SECTION}): add white paper \"${TITLE}\"" || { red "FAIL: nothing to commit"; echo exit_code=6; exit 6; }
git push -q -u origin "$BRANCH" || { red "FAIL: push rejected. Check repo write access."; echo exit_code=7; exit 7; }

# PR body from meta + sources
BODY=$(python3 - "$PDIR" "$TITLE" "$SECTION" "${PAGES:-unknown}" <<'PY'
import sys,json,os
pdir,title,section,pages=sys.argv[1:5]
sources=[]
sp=os.path.join(pdir,"sources.json")
if os.path.exists(sp):
    try:
        for s in json.load(open(sp)): sources.append(s.get("url",""))
    except Exception: pass
print(f"Summary: white paper added under research/{section}/.")
print(f"Section: {section}")
print(f"Build: PDF built yes, pages {pages}")
print("Sources:")
for u in sources: print(f"- {u}")
if not sources: print("- none")
print("Unverified claims: see the Limitations section in the paper.")
print("")
print("Reviewer checklist:")
for c in ["Section placement correct","Every claim traces to a real source or sits in Limitations","No secrets, PII, or private infrastructure","Links resolve (CI green)","Voice and public-safe framing acceptable"]:
    print(f"- [ ] {c}")
PY
)
gh pr create --base main --head "$BRANCH" --title "research(${SECTION}): ${TITLE}" --body "$BODY" 2>&1 | tee -a "$LOG"
rc=$?
[ "$rc" -eq 0 ] && say "PR opened" || red "PR step failed, see $LOG"
echo exit_code=$rc
exit $rc
