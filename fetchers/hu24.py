from .base import NewsSource
from .rss_utils import build_article, fetch_feed_entries


class Hu24Fetcher(NewsSource):

    RSS_URL = "https://24.hu/feed/"

    def fetch(self):
        entries = fetch_feed_entries(self.RSS_URL)
        return [build_article(entry, source="24.hu") for entry in entries if getattr(entry, "link", None)]
