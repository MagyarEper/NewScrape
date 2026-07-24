import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base


def load_env_file(file_path: str = ".env"):
    # Minimal .env reader to avoid extra dependency.
    env_path = Path(file_path)

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


load_env_file()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost/news",
)

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def create_database():
    """
    Creates tables if they don't exist.
    Safe to run multiple times.
    """
    Base.metadata.create_all(engine)