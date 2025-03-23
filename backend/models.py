from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class News(db.Model):
    """Model for storing scraped news data."""
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    headline = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    news_link = db.Column(db.String(255), nullable=True)
    last_updated = db.Column(db.String(100), nullable=True)
    tag = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<News {self.headline}>'


class SportsNews(db.Model):
    """Model for storing scraped sports news data."""
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    headline = db.Column(db.String(255))
    news_link = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(100))
    tag = db.Column(db.String(100), nullable=True)
    last_updated = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<SportsNews {self.headline}>'
