#!/usr/bin/env python3
"""
Zeid Data CloakCheck - Differential URL Fetch
Collects redirect chains + response metadata for the same URL across multiple "profiles".

Use only on URLs you are authorized to test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin

import requests
import tldextract

DEFAULT_UAS = [
    # Desktop-ish
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Mobile-ish
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
]

DEFAULT_LANGS = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "es-ES,es;q=0.9,en;q=0.6",
    "fr-FR,fr;q=0.9,en;q=0.6",
]

DEFAULT_REFERRERS = [
    "",  # no referrer
    "https://mail.google.com/",
    "https://outlook.office.com/",
    "https://duckduckgo.com/",
    "https://www.google.com/",
]

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

@dataclass
class RedirectHop:
    url: str
    status_code: int
    location: str

@dataclass
class FetchResult:
    run_id: str
    timestamp_utc: str
    input_url: str
    final_url: str
    method: str
    ua: str
    accept_language: str
    referrer: str
    status_code: int
    elapsed_ms: int
    redirect_chain: List[RedirectHop]
    headers: Dict[str, str]
    content_type: str
    content_length: int
    sha256: str
    title: str
    body_preview: str
    registrable_domain: str
    notes: str

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def safe_preview(text: str, limit: int = 280) -> str:
    # Remove whitespace noise and truncate.
    t = re.sub(r"\s+", " ", text).strip()
    return t[:limit]

def extract_title(html: str) -> str:
    m = TITLE_RE.search(html)
    if not m:
        return ""
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    return title[:200]

def get_registrable_domain(url: str) -> str:
    try:
        ext = tldextract.extract(url)
        if ext.registered_domain:
            return ext.registered_domain
    except Exception:
        pass
    # fallback
    p = urlparse(url)
    return p.hostname or ""

def build_profiles(count: int, seed: Optional[int] = None) -> List[Tuple[str, str, str]]:
    rnd = random.Random(seed)
    profiles = []
    for _ in range(count):
        ua = rnd.choice(DEFAULT_UAS)
        lang = rnd.choice(DEFAULT_LANGS)
        ref = rnd.choice(DEFAULT_REFERRERS)
        profiles.append((ua, lang, ref))
    return profiles

def fetch_once(url: str, ua: str, lang: str, ref: str, timeout: int, verify_tls: bool) -> FetchResult:
    headers = {
        "User-Agent": ua,
        "Accept-Language": lang,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "close",
    }
    if ref:
        headers["Referer"] = ref

    session = requests.Session()
    # Don't auto-follow redirects so we can capture every hop.
    chain: List[RedirectHop] = []
    start = time.time()
    current = url
    notes = ""

    for _ in range(10):  # max hops
        r = session.get(current, headers=headers, allow_redirects=False, timeout=timeout, verify=verify_tls)
        loc = r.headers.get("Location", "")
        status = int(r.status_code)
        if status in (301, 302, 303, 307, 308) and loc:
            next_url = urljoin(current, loc)
            chain.append(RedirectHop(url=current, status_code=status, location=next_url))
            current = next_url
            continue
        # terminal response
        elapsed_ms = int((time.time() - start) * 1000)
        body = r.content or b""
        ctype = r.headers.get("Content-Type", "")
        clen = int(r.headers.get("Content-Length") or len(body))
        title = ""
        preview = ""
        if "html" in ctype.lower() and body:
            try:
                text = body.decode(r.encoding or "utf-8", errors="replace")
                title = extract_title(text)
                preview = safe_preview(text)
            except Exception:
                notes = "html_decode_failed"
        result = FetchResult(
            run_id=f"run_{int(time.time()*1000)}",
            timestamp_utc=utc_now(),
            input_url=url,
            final_url=current,
            method="GET",
            ua=ua,
            accept_language=lang,
            referrer=ref,
            status_code=status,
            elapsed_ms=elapsed_ms,
            redirect_chain=chain,
            headers={k: str(v) for k, v in r.headers.items()},
            content_type=ctype,
            content_length=clen,
            sha256=sha256_bytes(body),
            title=title,
            body_preview=preview,
            registrable_domain=get_registrable_domain(current),
            notes=notes,
        )
        return result

    # too many redirects
    elapsed_ms = int((time.time() - start) * 1000)
    return FetchResult(
        run_id=f"run_{int(time.time()*1000)}",
        timestamp_utc=utc_now(),
        input_url=url,
        final_url=current,
        method="GET",
        ua=ua,
        accept_language=lang,
        referrer=ref,
        status_code=0,
        elapsed_ms=elapsed_ms,
        redirect_chain=chain,
        headers={},
        content_type="",
        content_length=0,
        sha256="",
        title="",
        body_preview="",
        registrable_domain=get_registrable_domain(current),
        notes="max_redirect_hops_exceeded",
    )

def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return ""
    if not re.match(r"^https?://", u, re.IGNORECASE):
        u = "http://" + u
    return u

def main() -> int:
    ap = argparse.ArgumentParser(description="Zeid Data CloakCheck: differential URL fetch")
    ap.add_argument("--url", help="Single URL to fetch")
    ap.add_argument("--infile", help="File containing URLs (one per line)")
    ap.add_argument("--out", default="runs", help="Output directory")
    ap.add_argument("--profiles", type=int, default=6, help="Number of randomized profiles to test per URL")
    ap.add_argument("--seed", type=int, default=1337, help="Random seed for profile selection")
    ap.add_argument("--timeout", type=int, default=20, help="HTTP timeout seconds")
    ap.add_argument("--no-verify-tls", action="store_true", help="Disable TLS verification (not recommended)")
    args = ap.parse_args()

    if not args.url and not args.infile:
        ap.error("Provide --url or --infile")

    urls: List[str] = []
    if args.url:
        urls.append(args.url)
    if args.infile:
        with open(args.infile, "r", encoding="utf-8") as f:
            for line in f:
                u = normalize_url(line)
                if u:
                    urls.append(u)

    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    verify_tls = not args.no_verify_tls
    profiles = build_profiles(args.profiles, seed=args.seed)

    for url in urls:
        url_n = normalize_url(url)
        if not url_n:
            continue

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_host = re.sub(r"[^a-zA-Z0-9._-]+", "_", urlparse(url_n).netloc or "url")
        base_name = f"zeid_data_cloakcheck_{safe_host}_{stamp}"

        results: List[dict] = []
        for i, (ua, lang, ref) in enumerate(profiles, start=1):
            try:
                res = fetch_once(url_n, ua, lang, ref, timeout=args.timeout, verify_tls=verify_tls)
                d = asdict(res)
                # expand redirect hops into dicts
                d["redirect_chain"] = [asdict(h) for h in res.redirect_chain]
                d["profile_index"] = i
                results.append(d)
                print(f"[{safe_host}] profile {i}/{len(profiles)} status={res.status_code} final={res.final_url}")
            except requests.RequestException as e:
                results.append({
                    "run_id": f"run_{int(time.time()*1000)}",
                    "timestamp_utc": utc_now(),
                    "input_url": url_n,
                    "error": str(e),
                    "profile_index": i,
                })
                print(f"[{safe_host}] profile {i}/{len(profiles)} ERROR: {e}", file=sys.stderr)

        out_path = os.path.join(out_dir, base_name + ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"url": url_n, "profiles_tested": len(profiles), "results": results}, f, indent=2)
        print(f"Saved: {out_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
