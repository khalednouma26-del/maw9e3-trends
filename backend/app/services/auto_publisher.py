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


def _is_article_worthy(keyword: str) -> bool:
    kw = keyword.strip()
    if len(kw) < 3 or len(kw) > 60:
        return False
    if "???" in kw:
        return False
    if len(kw.split()) > 8:
        return False
    if " - " in kw:
        return False
    if kw.lower() in {
        "try searching to get started", "home", "playback", "keyboard shortcuts", "history",
        "settings", "sign in", "about", "contact us", "terms", "privacy", "search",
    }:
        return False
    return True


ARTICLES_PER_KEYWORD = 3


class AutoPublisher:
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.trend_discovery = TrendDiscoveryService()
        self.strategy = ContentStrategy()

    async def run_full_pipeline(self, db: AsyncSession) -> dict:
        result = {"trends_fetched": 0, "articles_generated": 0, "articles_published": 0}

        # Step 1: Discover trends
        trends = await self.trend_discovery.discover_all()
        upserted = 0
        duplicates_removed = 0
        for t in trends:
            rows = (await db.execute(select(Trend).where(Trend.keyword == t["keyword"]))).scalars().all()
            if not rows:
                db.add(Trend(**t))
                continue
            row = rows[0]
            # Refresh live metrics (Google Trends volumes/scores change hourly)
            for field in ("score", "search_volume", "category", "url", "seo_keywords"):
                if t.get(field) is not None:
                    setattr(row, field, t[field])
            row.fetched_at = datetime.utcnow()
            upserted += 1
            # Clean up any duplicate rows (races between scheduler and manual runs)
            for extra in rows[1:]:
                await db.delete(extra)
                duplicates_removed += 1
        await db.commit()
        result["trends_fetched"] = len(trends)
        result["trends_updated"] = upserted
        result["trends_duplicates_removed"] = duplicates_removed

        # Step 2: Score and prioritize trends by niche relevance
        all_trends = (await db.execute(select(Trend).order_by(Trend.score.desc()).limit(200))).scalars().all()

        # Boost focus niche trends + prefer real Google Trends search queries
        scored = []
        for t in all_trends:
            niche_score = self.strategy.score_trend_for_niche(t.keyword, t.category)
            source_bonus = 10 if t.source == "google_trends" else 0
            scored.append((t.score + niche_score + source_bonus, t))
        scored.sort(key=lambda x: -x[0])

        trend_rows = []
        seen_cats = set()
        for _, t in scored:
            cat = t.category or "general"
            if cat not in seen_cats or len(trend_rows) < 25:
                trend_rows.append(t)
                seen_cats.add(cat)
        for trend in trend_rows[:40]:
            if not _is_article_worthy(trend.keyword):
                continue
            article_rows = (await db.execute(select(Article).where(Article.trend_keyword == trend.keyword))).scalars().all()
            # Trim any excess articles for this keyword down to the cap
            for extra in article_rows[ARTICLES_PER_KEYWORD:]:
                await db.delete(extra)
            num_existing = min(len(article_rows), ARTICLES_PER_KEYWORD)

            for i in range(num_existing, ARTICLES_PER_KEYWORD):
                article_data = await self.content_gen.generate_article(trend.keyword, trend.language or "en", trend.category, template_index=i)
                if not article_data:
                    continue

                slug = self.content_gen._slugify(article_data.get("title", trend.keyword))
                if i > 0:
                    slug = f"{slug[:195]}-{i + 1}"
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
                    published_at=datetime.utcnow(),
                )
                db.add(article)
                result["articles_generated"] += 1

        await db.commit()
        result["articles_published"] = result["articles_generated"]
        return result

    async def publish_drafts(self, db: AsyncSession) -> int:
        result = await db.execute(select(Article).where(Article.published == 0))
        drafts = result.scalars().all()
        now = datetime.utcnow()
        for article in drafts:
            article.published = 1
            article.published_at = now
            article.status = "published"
        await db.commit()
        return len(drafts)
