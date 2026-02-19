#!/usr/bin/env python3
"""
bundle_evidence.py
Create an evidence bundle zip with a SHA256 manifest.

This is designed for audit and incident evidence packs.

Usage:
  python scripts/bundle_evidence.py --input sample_data --output out/evidence_bundle.zip --label "q1_review"
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import zipfile
from datetime import datetime, timezone

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Folder to include")
    ap.add_argument("--output", required=True, help="Output zip path")
    ap.add_argument("--label", default="evidence", help="Bundle label")
    ap.add_argument("--include", default=".*", help="Regex of files to include, default all")
    args = ap.parse_args()

    in_dir = Path(args.input).resolve()
    out_zip = Path(args.output).resolve()
    out_zip.parent.mkdir(parents=True, exist_ok=True)

    include_re = args.include

    manifest = {
        "bundle_label": args.label,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(in_dir),
        "files": []
    }

    files = []
    for p in sorted(in_dir.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(in_dir).as_posix()
        if not __import__("re").match(include_re, rel):
            continue
        files.append((p, rel))

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # add files
        for p, rel in files:
            z.write(p, arcname=rel)
            manifest["files"].append({
                "path": rel,
                "bytes": p.stat().st_size,
                "sha256": sha256_file(p),
                "mtime_utc": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()
            })

        # add manifest inside zip
        manifest_json = json.dumps(manifest, indent=2).encode("utf-8")
        z.writestr("evidence_manifest.json", manifest_json)

        # add sha256 of the manifest
        mh = hashlib.sha256(manifest_json).hexdigest()
        z.writestr("evidence_manifest.sha256", mh + "  evidence_manifest.json\n")

    print(f"Created: {out_zip}")
    print(f"Files:   {len(manifest['files'])}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
