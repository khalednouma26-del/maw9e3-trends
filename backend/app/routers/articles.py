from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc

from app.config import settings
from app.database import get_db
from app.models.article import Article
from app.services.content_generator import ContentGenerator
from app.services.auto_publisher import AutoPublisher
from app.services.seo_service import SEOService
from app.services.trend_discovery import TrendDiscoveryService

router = APIRouter(prefix="/api/articles", tags=["articles"])
content_gen = ContentGenerator()
publisher = AutoPublisher()
seo = SEOService()


@router.get("/")
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Article).where(Article.published == 1)
    if category:
        query = query.where(Article.category_name == category)
    if search:
        query = query.where(
            or_(Article.title.ilike(f"%{search}%"), Article.summary.ilike(f"%{search}%"))
        )
    query = query.order_by(Article.published_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    articles = result.scalars().all()

    count_q = select(Article).where(Article.published == 1)
    if category:
        count_q = count_q.where(Article.category_name == category)
    if search:
        count_q = count_q.where(
            or_(Article.title.ilike(f"%{search}%"), Article.summary.ilike(f"%{search}%"))
        )
    total = len((await db.execute(count_q)).scalars().all())

    return {
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "slug": a.slug,
                "summary": a.summary,
                "excerpt": a.excerpt,
                "trend_keyword": a.trend_keyword,
                "category_name": a.category_name,
                "tags": a.tags,
                "image_url": a.image_url,
                "word_count": a.word_count,
                "view_count": a.view_count,
                "published_at": str(a.published_at) if a.published_at else None,
            }
            for a in articles
        ],
        "page": page,
        "per_page": per_page,
        "total": total,
    }


@router.get("/{article_id}")
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.view_count = (article.view_count or 0) + 1
    await db.commit()

    # Related articles (same category, exclude self)
    rel_q = select(Article).where(Article.category_name == article.category_name, Article.id != article_id, Article.published == 1).order_by(desc(Article.published_at)).limit(4)
    related = (await db.execute(rel_q)).scalars().all()

    article_schema = seo.generate_schema_article({
        "id": article.id, "title": article.title, "meta_title": article.meta_title,
        "meta_description": article.meta_description, "image_url": article.image_url,
        "published_at": str(article.published_at) if article.published_at else None,
        "updated_at": str(article.updated_at), "tags": article.tags,
        "category_name": article.category_name, "word_count": article.word_count,
    })
    breadcrumb_schema = seo.generate_breadcrumb_schema([
        {"name": "Home", "item": settings.site_url},
        {"name": article.category_name.capitalize() if article.category_name else "Articles", "item": f"{settings.site_url}/?category={article.category_name}" if article.category_name else settings.site_url},
        {"name": article.title[:60], "item": f"{settings.site_url}/article/{article.id}"},
    ])

    return {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "content": article.content,
        "summary": article.summary,
        "meta_title": article.meta_title,
        "meta_description": article.meta_description,
        "excerpt": article.excerpt,
        "tags": article.tags,
        "category_name": article.category_name,
        "trend_keyword": article.trend_keyword,
        "image_url": article.image_url,
        "image_alt": article.image_alt,
        "word_count": article.word_count,
        "faq_schema": article.faq_schema,
        "view_count": article.view_count,
        "published": article.published,
        "published_at": str(article.published_at) if article.published_at else None,
        "created_at": str(article.created_at),
        "schema": article_schema,
        "breadcrumb_schema": breadcrumb_schema,
        "related_articles": [
            {
                "id": r.id, "title": r.title, "slug": r.slug,
                "excerpt": r.excerpt or r.summary,
                "image_url": r.image_url, "image_alt": r.image_alt,
                "published_at": str(r.published_at) if r.published_at else None,
                "view_count": r.view_count, "category_name": r.category_name,
            }
            for r in related
        ],
    }


@router.post("/generate")
async def generate_articles(db: AsyncSession = Depends(get_db)):
    result = await publisher.run_full_pipeline(db)
    return result


@router.post("/publish")
async def publish_drafts(db: AsyncSession = Depends(get_db)):
    count = await publisher.publish_drafts(db)
    return {"message": f"Published {count} articles", "count": count}
