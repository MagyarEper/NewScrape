from sqlalchemy.exc import IntegrityError

from models.models import Article


class ArticleRepository:

    def __init__(self, session):
        self.session = session

    def save_articles(self, articles):
        inserted = 0
        duplicates = 0

        for article in articles:

            db_article = Article(**article)

            self.session.add(db_article)

            try:
                self.session.commit()
                inserted += 1

            except IntegrityError:
                # URL already exists
                self.session.rollback()
                duplicates += 1

        return {
            "inserted": inserted,
            "duplicates": duplicates,
        }