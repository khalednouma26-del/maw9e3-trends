from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(500), index=True)
    source = Column(String(50))
    score = Column(Float, default=0.0)
    search_volume = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    language = Column(String(10), default="en")
    intent = Column(String(50), nullable=True)
    seo_keywords = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
