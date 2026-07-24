from datetime import datetime

import feedparser
import httpx


def _to_datetime(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])

    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])

    return None


def _extract_category(entry, fallback=None):
    if hasattr(entry, "tags") and entry.tags:
        return getattr(entry.tags[0], "term", fallback)

    return fallback


def build_article(entry, source, default_category=None):
    return {
        "source": source,
        "title": getattr(entry, "title", "Untitled"),
        "url": getattr(entry, "link", ""),
        "summary": getattr(entry, "summary", None),
        "published": _to_datetime(entry),
        "author": getattr(entry, "author", None),
        "category": _extract_category(entry, fallback=default_category),
        "content": None,
    }


def fetch_feed_entries(rss_url):
    response = httpx.get(rss_url, timeout=15)
    response.raise_for_status()
    feed = feedparser.parse(response.text)
    return feed.entries
