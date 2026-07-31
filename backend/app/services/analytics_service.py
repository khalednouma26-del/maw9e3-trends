from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date

from app.models.analytics import AnalyticsEvent
from app.models.article import Article


class AnalyticsService:
    async def track_event(self, db: AsyncSession, event_type: str, **kwargs):
        event = AnalyticsEvent(
            event_type=event_type,
            article_id=kwargs.get("article_id"),
            page_url=kwargs.get("page_url"),
            referrer=kwargs.get("referrer"),
            user_agent=kwargs.get("user_agent"),
            ip_address=kwargs.get("ip_address"),
            country=kwargs.get("country"),
            duration_seconds=kwargs.get("duration_seconds"),
        )
        db.add(event)
        await db.commit()

    async def get_dashboard_stats(self, db: AsyncSession) -> dict:
        now = datetime.now(timezone.utc)
        today = now.date()
        week_ago = today - timedelta(days=7)

        total_views = await db.scalar(select(func.count(AnalyticsEvent.id)).where(AnalyticsEvent.event_type == "page_view"))
        total_views = total_views or 0

        today_views = await db.scalar(
            select(func.count(AnalyticsEvent.id))
            .where(AnalyticsEvent.event_type == "page_view")
            .where(cast(AnalyticsEvent.created_at, Date) == today)
        )
        today_views = today_views or 0

        unique_visitors = await db.scalar(
            select(func.count(func.distinct(AnalyticsEvent.ip_address)))
            .where(AnalyticsEvent.event_type == "page_view")
        )
        unique_visitors = unique_visitors or 0

        total_articles = await db.scalar(select(func.count(Article.id)))
        total_articles = total_articles or 0

        published_articles = await db.scalar(select(func.count(Article.id)).where(Article.published == 1))
        published_articles = published_articles or 0

        recent_views = await db.scalar(
            select(func.count(AnalyticsEvent.id))
            .where(AnalyticsEvent.event_type == "page_view")
            .where(cast(AnalyticsEvent.created_at, Date) >= week_ago)
        )
        recent_views = recent_views or 0

        return {
            "total_views": total_views,
            "today_views": today_views,
            "unique_visitors": unique_visitors,
            "total_articles": total_articles,
            "published_articles": published_articles,
            "recent_views_7d": recent_views,
            "draft_articles": total_articles - published_articles,
        }

    async def get_recent_events(self, db: AsyncSession, limit: int = 50) -> list[AnalyticsEvent]:
        result = await db.execute(
            select(AnalyticsEvent).order_by(AnalyticsEvent.created_at.desc()).limit(limit)
        )
        return result.scalars().all()
