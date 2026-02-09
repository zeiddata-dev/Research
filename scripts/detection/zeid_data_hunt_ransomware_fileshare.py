"""
hunt_ransomware_fileshare.py
Detection-only sweep: scans a directory tree for common ransom note filenames and
identifies bursts of a single "unknown" extension in the last N hours.

Usage:
  python hunt_ransomware_fileshare.py --root "\\\\fileserver\\share" --hours 24 --top 10
  python hunt_ransomware_fileshare.py --root "/mnt/share" --hours 24 --top 10
"""

import argparse
import os
import time
from collections import Counter, defaultdict

DEFAULT_NOTE_NAMES = {
    "readme.txt", "readme.html", "how_to_decrypt.txt", "how_to_recover.txt",
    "recover_files.txt", "restore_files.txt", "decrypt_files.txt", "readme_to_decrypt.txt"
}

COMMON_EXT_ALLOW = {  # baseline allowlist; tune to your environment
    ".txt",".log",".csv",".json",".xml",".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx",
    ".jpg",".jpeg",".png",".gif",".tif",".tiff",".bmp",".zip",".7z",".rar",".tar",".gz",
    ".exe",".dll",".sys",".msi",".lnk",".ps1",".bat",".cmd",".sh",".py"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Root path to scan (file share mount or UNC path)")
    ap.add_argument("--hours", type=int, default=24, help="Lookback window in hours")
    ap.add_argument("--top", type=int, default=10, help="Top N suspicious extensions to show")
    args = ap.parse_args()

    cutoff = time.time() - (args.hours * 3600)

    ransom_notes = []
    ext_counter = Counter()
    ext_by_dir = defaultdict(Counter)

    for dirpath, _, filenames in os.walk(args.root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                st = os.stat(full)
            except OSError:
                continue

            if st.st_mtime < cutoff:
                continue

            low = fn.lower()
            if low in DEFAULT_NOTE_NAMES or ("decrypt" in low and low.endswith((".txt",".html",".hta"))):
                ransom_notes.append(full)

            _, ext = os.path.splitext(low)
            if ext and ext not in COMMON_EXT_ALLOW:
                ext_counter[ext] += 1
                ext_by_dir[dirpath][ext] += 1

    print(f"\n[+] Lookback: last {args.hours} hour(s)")
    print(f"[+] Root: {args.root}\n")

    if ransom_notes:
        print("[!] Possible ransom notes found:")
        for p in ransom_notes[:50]:
            print(f"  - {p}")
        if len(ransom_notes) > 50:
            print(f"  ... ({len(ransom_notes) - 50} more)")
    else:
        print("[+] No obvious ransom note filenames found in lookback window.")

    print("\n[!] Top suspicious extensions (not in allowlist):")
    for ext, cnt in ext_counter.most_common(args.top):
        print(f"  - {ext}: {cnt} file(s)")

    print("\n[!] Hot directories (top 5 dirs by suspicious ext volume):")
    hot = sorted(ext_by_dir.items(), key=lambda kv: sum(kv[1].values()), reverse=True)[:5]
    for d, c in hot:
        common = ", ".join([f"{e}:{n}" for e, n in c.most_common(3)])
        print(f"  - {d}  ({common})")

if __name__ == "__main__":
    main()
