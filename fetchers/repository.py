from sqlalchemy.exc import IntegrityError

from models.models import Article


class ArticleRepository:

    def __init__(self, session):
        self.session = session

    def save_articles(self, articles):

        for article in articles:

            db_article = Article(**article)

            self.session.add(db_article)

            try:
                self.session.commit()

            except IntegrityError:
                # URL already exists
                self.session.rollback()