# White paper pipeline

Automated drafting and placement of white papers into `research/<section>/`,
with a human pull request gate. No paper reaches `main` without review.

## One time setup
```
tools/scripts/zd_whitepaper_bootstrap.sh --with-tectonic
```
Vendors the OFL brand fonts (DM Serif Display, Inter) into
`templates/whitepaper/fonts/`, writes checksums, and installs `tectonic`.
The fonts are local only and are not committed. Re-run on any new machine.

## Drafting a paper
Feed the operating prompt at `tools/whitepaper-agent.md` to your command-line
research agent, with either a topic or a path to source material:
```
<topic string>            # generate mode: research and cite
path/to/notes.md          # transform mode: build from existing material
```
The agent classifies the section, drafts with cited sources, builds the PDF,
and opens a PR into `main`. The agent never merges.

Once a paper folder exists at `research/<section>/<slug>/`, you can build it,
branch, commit, push, and open the PR in one command:
```
tools/scripts/zd_whitepaper_ship.sh research/<section>/<slug>
```
It reads the title and section from `meta.yml`, assembles the PR body from
`sources.json`, refuses to run on a dirty tree, and never merges.

## Drafting in a Codespace (no local clone)

If the repo is too large to keep on your machine, draft in the cloud. On the
repo, use the green Code button, open the Codespaces tab, and create a Codespace.
The devcontainer in `.devcontainer/` installs `tectonic` and vendors the brand
fonts on first create, so the build and bootstrap scripts work with no further
setup. From the Codespace terminal:
```
tools/scripts/zd_whitepaper_build.sh research/<section>/<slug>
```
The repo lives in the cloud, nothing is downloaded to your disk. To make startup
instant instead of a one minute setup, enable Codespaces prebuilds for the repo
in Settings, Codespaces.

## Building a paper by hand
```
tools/scripts/zd_whitepaper_build.sh research/<section>/<slug>
```
Detects the toolchain (tectonic, then latexmk, then xelatex), fails loud if
none is present. PDF lands next to the source.

## Layout contract
- Papers live at `research/<section>/<slug>/` (exactly three levels deep).
- Each paper folder holds `paper.tex`, `paper.pdf`, `sources.json`, `meta.yml`.
- `paper.tex` sets `\def\zdroot{../../../}` and includes the house preamble at
  `templates/whitepaper/zd-whitepaper.tex`.
- Every claim maps to a real URL in `sources.json`, or it sits in the mandatory
  "Limitations and Unverified Claims" section. Link-check CI enforces resolvable
  URLs.
