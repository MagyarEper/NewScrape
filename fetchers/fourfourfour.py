from .base import NewsSource
from .rss_utils import build_article, fetch_feed_entries


class FourFourFourFetcher(NewsSource):

    RSS_URL = "https://444.hu/feed"

    def fetch(self):
        entries = fetch_feed_entries(self.RSS_URL)
        return [build_article(entry, source="444.hu") for entry in entries if getattr(entry, "link", None)]
