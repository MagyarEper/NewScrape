import sys
import re
from pathlib import Path

from flask import Flask, render_template, request
from markupsafe import Markup, escape
from sqlalchemy import desc, func, or_
from sqlalchemy.exc import ProgrammingError

# Allow direct execution: python web/app.py
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.database import Session
from models.models import Article, ScrapeRun

app = Flask(__name__)


TAG_RE = re.compile(r"<[^>]+>")


def extract_search_terms(query_text):
    terms = []

    for term in query_text.split():
        normalized = term.strip().lower()

        if normalized and normalized not in terms:
            terms.append(normalized)

    return terms


def strip_html(value):
    return TAG_RE.sub("", value or "")


def truncate_text(value, max_len=260):
    if len(value) <= max_len:
        return value

    return value[: max_len - 3].rstrip() + "..."


def highlight_text(value, terms):
    escaped = str(escape(value or ""))

    if not terms:
        return Markup(escaped)

    pattern = re.compile("(" + "|".join(re.escape(term) for term in terms) + ")", re.IGNORECASE)
    highlighted = pattern.sub(r"<mark>\1</mark>", escaped)
    return Markup(highlighted)


@app.route("/")
def index():
    per_page = 100
    query_text = request.args.get("q", "").strip()
    source_filter = request.args.get("source", "").strip()

    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1

    page = max(page, 1)
    search_terms = extract_search_terms(query_text)

    session = Session()
    last_scrape_run = None

    try:
        try:
            last_scrape_run = (
                session.query(ScrapeRun)
                .order_by(desc(ScrapeRun.ran_at), desc(ScrapeRun.id))
                .first()
            )
        except ProgrammingError:
            # Table may not exist before first scrape on a fresh database.
            session.rollback()

        sources = [
            row[0]
            for row in session.query(Article.source)
            .distinct()
            .order_by(Article.source.asc())
            .all()
        ]

        base_query = session.query(Article)

        if source_filter:
            base_query = base_query.filter(Article.source == source_filter)

        if query_text:
            like_pattern = f"%{query_text}%"
            base_query = base_query.filter(
                or_(
                    Article.title.ilike(like_pattern),
                    Article.summary.ilike(like_pattern),
                )
            )

        total_count = base_query.with_entities(func.count(Article.id)).scalar() or 0
        total_pages = max((total_count + per_page - 1) // per_page, 1)
        page = min(page, total_pages)

        articles = (
            base_query
            .order_by(desc(Article.published), desc(Article.id))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        for article in articles:
            summary_plain = truncate_text(strip_html(article.summary or ""))
            article.display_title = highlight_text(article.title or "Untitled", search_terms)
            article.display_summary = highlight_text(summary_plain, search_terms) if summary_plain else None

        page_start = max(page - 2, 1)
        page_end = min(page + 2, total_pages)
        page_numbers = list(range(page_start, page_end + 1))
    finally:
        session.close()

    return render_template(
        "index.html",
        articles=articles,
        query_text=query_text,
        source_filter=source_filter,
        sources=sources,
        page=page,
        per_page=per_page,
        total_count=total_count,
        total_pages=total_pages,
        page_numbers=page_numbers,
        last_scrape_run=last_scrape_run,
    )


if __name__ == "__main__":
    app.run(debug=True)
