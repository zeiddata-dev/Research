#!/usr/bin/env python3
from __future__ import annotations

import compileall
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]

SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "_archived_duplicate_repos",
}

SECRET_PATTERNS = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b")),
]

TEXT_EXTS = {
    ".md", ".txt", ".py", ".sh", ".ps1", ".yml", ".yaml", ".json", ".toml",
    ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".xml", ".svg", ".csv",
}

def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode != 0:
        print(p.stdout, end="")
        raise RuntimeError("command failed: " + " ".join(cmd))
    return p

def tracked_files() -> list[Path]:
    out = run(["git", "ls-files"]).stdout.splitlines()
    return [ROOT / line for line in out if line.strip()]

def skipped(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    return any(part in SKIP_PARTS for part in rel_parts)

def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS

def extract_links(text: str) -> list[str]:
    links: list[str] = []
    links += re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
    links += [x for pair in re.findall(r'<a\s+[^>]*href="([^"]+)"|<img\s+[^>]*src="([^"]+)"', text) for x in pair if x]
    return links

def local_link_ok(md_file: Path, target: str) -> bool:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto", "tel", "data"}:
        return True

    clean = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean or clean.startswith("#"):
        return True

    return (md_file.parent / unquote(clean)).resolve().exists()

def validate_root_readme() -> list[str]:
    errors: list[str] = []
    readme = ROOT / "README.md"

    if not readme.exists():
        return ["README.md missing"]

    text = readme.read_text(encoding="utf-8", errors="replace")

    required_markers = [
        "<!-- ZEID DATA README HERO START -->",
        "<!-- ZEID DATA README HERO END -->",
        "<!-- ZEID DATA LAB MAP START -->",
        "<!-- ZEID DATA LAB MAP END -->",
        "<!-- ZEID DATA TAGS START -->",
        "<!-- ZEID DATA TAGS END -->",
    ]

    for marker in required_markers:
        if text.count(marker) != 1:
            errors.append(f"README marker count invalid for {marker}: {text.count(marker)}")

    if text.count("## Lab Map") != 1:
        errors.append(f"expected exactly one '## Lab Map', found {text.count('## Lab Map')}")

    if "## Lab map" in text:
        errors.append("old lowercase '## Lab map' section is still present")

    for link in extract_links(text):
        if not local_link_ok(readme, link):
            errors.append(f"README broken local link: {link}")

    return errors

def validate_readme_hero_links() -> list[str]:
    errors: list[str] = []

    for path in tracked_files():
        if path.name.lower() != "readme.md":
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        hero = re.search(
            r"<!-- ZEID DATA README HERO START -->(.*?)<!-- ZEID DATA README HERO END -->",
            text,
            flags=re.DOTALL,
        )
        if not hero:
            continue

        for link in extract_links(hero.group(1)):
            if not local_link_ok(path, link):
                rel = path.relative_to(ROOT).as_posix()
                errors.append(f"{rel} broken hero link: {link}")

    return errors

def validate_python_compile() -> list[str]:
    errors: list[str] = []
    py_files = [p for p in tracked_files() if p.suffix == ".py" and not skipped(p)]

    if not py_files:
        return []

    for path in py_files:
        ok = compileall.compile_file(str(path), quiet=1)
        if not ok:
            errors.append(f"python compile failed: {path.relative_to(ROOT).as_posix()}")

    return errors

def validate_shell_syntax() -> list[str]:
    errors: list[str] = []
    sh_files = [p for p in tracked_files() if p.suffix == ".sh" and not skipped(p)]

    for path in sh_files:
        p = subprocess.run(["bash", "-n", str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            errors.append(f"bash syntax failed: {path.relative_to(ROOT).as_posix()}\n{p.stdout}")

    return errors

def validate_secret_patterns() -> list[str]:
    errors: list[str] = []

    for path in tracked_files():
        if skipped(path) or not path.is_file() or not is_text(path):
            continue

        rel = path.relative_to(ROOT).as_posix()

        if rel.startswith("scripts/ci/validate_repo_quality.py"):
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if "example" in low or "placeholder" in low or "dummy" in low:
                continue
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    errors.append(f"secret-like value found: {name} {rel}:{lineno}")

    return errors

def main() -> int:
    checks = {
        "root_readme": validate_root_readme(),
        "readme_hero_links": validate_readme_hero_links(),
        "python_compile": validate_python_compile(),
        "shell_syntax": validate_shell_syntax(),
        "secret_patterns": validate_secret_patterns(),
    }

    failed = False
    for name, errors in checks.items():
        if errors:
            failed = True
            print(f"[FAIL] {name}")
            for error in errors[:80]:
                print(f"  {error}")
            if len(errors) > 80:
                print(f"  ... {len(errors) - 80} more")
        else:
            print(f"[PASS] {name}")

    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
