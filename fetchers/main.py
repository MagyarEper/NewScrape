import sys
from pathlib import Path

from sqlalchemy.exc import OperationalError

# Allow direct execution: python fetchers/main.py
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.database import Session, create_database

from fetchers.fourfourfour import FourFourFourFetcher
from fetchers.hvg import HvgFetcher
from fetchers.repository import ArticleRepository
from fetchers.hu24 import Hu24Fetcher
from fetchers.index_hu import IndexHuFetcher
from fetchers.portfolio import PortfolioFetcher
from fetchers.telex import TelexFetcher


def main():

    try:
        # Create tables (only the first run actually creates them)
        create_database()

        # Open a connection to PostgreSQL
        session = Session()
    except OperationalError as exc:
        print("Database connection error.")
        print("Set a valid DATABASE_URL environment variable, for example:")
        print("export DATABASE_URL='postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost/news'")
        print(f"Details: {exc}")
        return

    all_articles = []

    fetchers = [
        TelexFetcher(),
        Hu24Fetcher(),
        HvgFetcher(),
        IndexHuFetcher(),
        FourFourFourFetcher(),
        PortfolioFetcher(),
    ]

    for fetcher in fetchers:
        source_name = fetcher.__class__.__name__.replace("Fetcher", "")

        try:
            articles = fetcher.fetch()
        except Exception as exc:
            print(f"Failed to fetch from {source_name}: {exc}")
            continue

        all_articles.extend(articles)

        if articles:
            source_name = articles[0]["source"]

        print(f"Downloaded {len(articles)} articles from {source_name}")

    print(f"Downloaded {len(all_articles)} articles in total")

    # Save them
    repo = ArticleRepository(session)

    repo.save_articles(all_articles)

    print("Done!")


if __name__ == "__main__":
    main()