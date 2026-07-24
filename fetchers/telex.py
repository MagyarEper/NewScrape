from .base import NewsSource
from .rss_utils import build_article, fetch_feed_entries


class TelexFetcher(NewsSource):

    RSS_URL = "https://telex.hu/rss"

    def fetch(self):
        entries = fetch_feed_entries(self.RSS_URL)
        return [build_article(entry, source="Telex") for entry in entries if getattr(entry, "link", None)]