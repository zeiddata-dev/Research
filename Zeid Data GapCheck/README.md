# Zeid Data GapCheck (Air‑Gap Network Compliance Evidence Collector)

An offline-first CLI tool that collects **host-based network evidence** to help prove an environment is *air‑gapped* (or to identify where it isn’t). It produces a timestamped evidence bundle (raw command output + normalized JSON + human‑readable Markdown) suitable for audit attachments.

## Quick start
```bash
python gapcheck.py run --policy policy.sample.json --output ./evidence
```

## Authorized use only
Run this tool only on systems and networks you are authorized to assess.
