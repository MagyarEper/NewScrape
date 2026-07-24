from .base import NewsSource
from .rss_utils import build_article, fetch_feed_entries


class PortfolioFetcher(NewsSource):

    RSS_URL = "https://www.portfolio.hu/rss/all.xml"

    def fetch(self):
        entries = fetch_feed_entries(self.RSS_URL)
        return [build_article(entry, source="Portfolio") for entry in entries if getattr(entry, "link", None)]
