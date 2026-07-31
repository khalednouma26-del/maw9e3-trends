from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Integer as Int
from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    slug = Column(String(500), unique=True, index=True)
    content = Column(Text)
    summary = Column(Text)
    meta_title = Column(String(500), nullable=True)
    meta_description = Column(String(1000), nullable=True)
    excerpt = Column(String(1000), nullable=True)
    tags = Column(Text, nullable=True)
    category_id = Column(Integer, nullable=True)
    category_name = Column(String(100), nullable=True)
    trend_keyword = Column(String(500), nullable=True)
    image_url = Column(String(1000), nullable=True)
    image_alt = Column(String(500), nullable=True)
    language = Column(String(10), default="en")
    word_count = Column(Integer, default=0)
    faq_schema = Column(Text, nullable=True)
    status = Column(String(20), default="draft")
    published = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    published_at = Column(DateTime, nullable=True)
