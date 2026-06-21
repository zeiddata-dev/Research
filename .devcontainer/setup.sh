#!/usr/bin/env bash
# Codespace setup. Makes tectonic and the brand fonts ready so the build and
# bootstrap scripts run with no further steps. Runs once when the Codespace is
# created. Safe to re-run.
mkdir -p "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
bash tools/scripts/zd_whitepaper_bootstrap.sh --with-tectonic
echo ""
echo "Codespace ready."
echo "Build a paper:  tools/scripts/zd_whitepaper_build.sh research/<section>/<slug>"
echo "Draft a paper:  feed tools/whitepaper-agent.md to your command-line agent"
