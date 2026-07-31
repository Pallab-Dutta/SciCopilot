#!/usr/bin/env python3
"""Ping IndexNow with the URLs that just changed, read from a built sitemap.

IndexNow (https://www.indexnow.org) tells Bing/Yandex/Seznam/Naver to re-crawl
a URL immediately. Bing's index is what ChatGPT Search and Copilot retrieve from,
so fast IndexNow submission is the durable GEO win: a new post is retrievable by
generative engines within minutes instead of waiting days for an organic crawl.

Why a time window instead of "submit everything":
  The site rebuilds HOURLY to release scheduled posts, but most hourly builds
  change nothing. Submitting the whole sitemap every hour is exactly the abuse
  IndexNow warns against. So we submit only URLs whose sitemap <lastmod> is within
  the last WINDOW_HOURS. On a quiet hour that set is empty and we send nothing.
  When a post publishes (by push, lastmod≈now; or by the cron crossing its
  publishDate, lastmod≈release time) it and the index/taxonomy pages it touched
  fall inside the window and get submitted, for a few hours, then drop out.

Note: editing an old post does NOT bump its <lastmod> (Hugo's Lastmod defaults to
the front-matter date), so pure edits are not caught here — submit those by hand
in Bing Webmaster Tools' "Submit URLs" tile if they need urgent re-crawl.

Indexing is best-effort: any failure prints a warning and exits 0 so a flaky
IndexNow endpoint can never fail a deploy.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

API = "https://api.indexnow.org/indexnow"
_SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def _parse_lastmod(text: str) -> datetime | None:
    """Parse a sitemap <lastmod>, tolerating both full timestamps and bare dates.
    A bare date (no time zone) is treated as UTC midnight."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        try:
            dt = datetime.strptime(text[:10], "%Y-%m-%d")
        except ValueError:
            return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def recent_urls(sitemap: Path, host: str, cutoff: datetime) -> list[str]:
    if not sitemap.is_file():
        return []
    try:
        root = ET.fromstring(sitemap.read_text(encoding="utf-8"))
    except (OSError, ET.ParseError) as exc:
        print(f"[indexnow] could not read {sitemap}: {exc}", file=sys.stderr)
        return []
    out: list[str] = []
    for url in root.findall(f"{_SM_NS}url"):
        loc = (url.findtext(f"{_SM_NS}loc") or "").strip()
        lastmod = _parse_lastmod(url.findtext(f"{_SM_NS}lastmod") or "")
        if not loc or lastmod is None or lastmod < cutoff:
            continue
        if urlsplit(loc).netloc != host:   # never submit a URL off this host
            continue
        out.append(loc)
    return out


def main() -> int:
    host = os.environ["INDEXNOW_HOST"].strip()
    key = os.environ["INDEXNOW_KEY"].strip()
    window_hours = float(os.environ.get("INDEXNOW_WINDOW_HOURS", "3"))
    sitemaps = [Path(p) for p in sys.argv[1:]] or [Path("_site/blog/sitemap.xml")]

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    urls = sorted({u for sm in sitemaps for u in recent_urls(sm, host, cutoff)})

    if not urls:
        print(f"[indexnow] nothing changed in the last {window_hours:g}h — skipping.")
        return 0

    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }
    print(f"[indexnow] submitting {len(urls)} URL(s):")
    for u in urls:
        print(f"           {u}")

    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"[indexnow] endpoint returned HTTP {resp.status}")
    except Exception as exc:  # best-effort: never fail the deploy over indexing
        print(f"[indexnow] WARNING: submission failed ({exc}). Continuing.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
