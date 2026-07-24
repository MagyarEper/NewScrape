from .base import NewsSource
from .rss_utils import build_article, fetch_feed_entries


class IndexHuFetcher(NewsSource):

    RSS_URL = "https://index.hu/24ora/rss/"

    def fetch(self):
        entries = fetch_feed_entries(self.RSS_URL)
        return [build_article(entry, source="Index") for entry in entries if getattr(entry, "link", None)]
