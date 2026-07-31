import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update

from app.models.article import Article
from app.models.trend import Trend
from app.services.content_generator import ContentGenerator
from app.services.trend_discovery import TrendDiscoveryService
from app.services.content_strategy import ContentStrategy

logger = logging.getLogger("maw9e3.publisher")


class AutoPublisher:
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.trend_discovery = TrendDiscoveryService()
        self.strategy = ContentStrategy()

    async def run_full_pipeline(self, db: AsyncSession) -> dict:
        result = {"trends_fetched": 0, "articles_generated": 0, "articles_published": 0}

        # Step 1: Discover trends
        trends = await self.trend_discovery.discover_all()
        for t in trends:
            existing = await db.execute(select(Trend).where(Trend.keyword == t["keyword"]))
            if not existing.scalar_one_or_none():
                db.add(Trend(**t))
        await db.commit()
        result["trends_fetched"] = len(trends)

        # Step 2: Score and prioritize trends by niche relevance
        all_trends = (await db.execute(select(Trend).order_by(Trend.score.desc()).limit(200))).scalars().all()

        # Boost focus niche trends
        scored = []
        for t in all_trends:
            niche_score = self.strategy.score_trend_for_niche(t.keyword, t.category)
            scored.append((t.score + niche_score, t))
        scored.sort(key=lambda x: -x[0])

        trend_rows = []
        seen_cats = set()
        for _, t in scored:
            cat = t.category or "general"
            if cat not in seen_cats or len(trend_rows) < 25:
                trend_rows.append(t)
                seen_cats.add(cat)
        for trend in trend_rows[:40]:
            existing = await db.execute(select(Article).where(Article.trend_keyword == trend.keyword))
            if existing.scalar_one_or_none():
                continue

            article_data = await self.content_gen.generate_article(trend.keyword, trend.language or "en", trend.category)
            if not article_data:
                continue

            slug = self.content_gen._slugify(article_data.get("title", trend.keyword))
            article = Article(
                title=article_data.get("title", trend.keyword),
                slug=slug,
                content=article_data.get("content", ""),
                summary=article_data.get("excerpt", "")[:1000],
                meta_title=article_data.get("meta_title", "")[:500],
                meta_description=article_data.get("meta_description", "")[:1000],
                excerpt=article_data.get("excerpt", "")[:1000],
                tags=article_data.get("tags", ""),
                trend_keyword=trend.keyword,
                faq_schema=article_data.get("faq_schema", ""),
                word_count=article_data.get("word_count", 0),
                status="published",
                published=1,
                image_url=article_data.get("image_url"),
                image_alt=article_data.get("image_alt"),
                category_name=trend.category,
                language=trend.language or "en",
                published_at=datetime.now(timezone.utc),
            )
            db.add(article)
            result["articles_generated"] += 1

        await db.commit()
        result["articles_published"] = result["articles_generated"]
        return result

    async def publish_drafts(self, db: AsyncSession) -> int:
        result = await db.execute(select(Article).where(Article.published == 0))
        drafts = result.scalars().all()
        now = datetime.now(timezone.utc)
        for article in drafts:
            article.published = 1
            article.published_at = now
            article.status = "published"
        await db.commit()
        return len(drafts)
