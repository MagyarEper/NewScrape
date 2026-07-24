import sys
from pathlib import Path

from flask import Flask, render_template, request
from sqlalchemy import desc, func, or_

# Allow direct execution: python web/app.py
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.database import Session
from models.models import Article

app = Flask(__name__)


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

    session = Session()

    try:
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
    )


if __name__ == "__main__":
    app.run(debug=True)
