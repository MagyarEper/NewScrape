from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Text, Integer


class Base(DeclarativeBase):
    """
    Every SQLAlchemy model will inherit from this.
    SQLAlchemy uses it to know which tables exist.
    """
    pass


class Article(Base):
    """
    Represents ONE article inside the database.
    """

    __tablename__ = "articles"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Name of the news portal
    source: Mapped[str] = mapped_column(String(50))

    # Article title
    title: Mapped[str] = mapped_column(String(500))

    # URL should be unique.
    # If Telex RSS returns the same article tomorrow,
    # PostgreSQL will reject duplicates.
    url: Mapped[str] = mapped_column(String(1000), unique=True)

    # RSS description
    summary: Mapped[str | None] = mapped_column(Text())

    # Publication date
    published = mapped_column(DateTime)

    # Optional author
    author: Mapped[str | None] = mapped_column(String(200))

    # Optional category
    category: Mapped[str | None] = mapped_column(String(100))

    # Full article text (None for now)
    content: Mapped[str | None] = mapped_column(Text())


class ScrapeRun(Base):
    """
    Stores metadata about each scraper execution.
    """

    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    ran_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_fetched: Mapped[int] = mapped_column(Integer)
    inserted: Mapped[int] = mapped_column(Integer)
    duplicates: Mapped[int] = mapped_column(Integer)