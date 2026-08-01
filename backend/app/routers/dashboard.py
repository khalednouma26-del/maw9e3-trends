from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.models.user import User
from app.models.article import Article
from app.models.trend import Trend
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
analytics = AnalyticsService()


@router.get("/stats")
async def dashboard_stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return await analytics.get_dashboard_stats(db)


@router.get("/events")
async def recent_events(limit: int = 50, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    events = await analytics.get_recent_events(db, limit)
    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "article_id": e.article_id,
            "page_url": e.page_url,
            "country": e.country,
            "created_at": str(e.created_at),
        }
        for e in events
    ]


@router.post("/cleanup-legacy-articles")
async def cleanup_legacy_articles(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    gt_keywords = set((await db.execute(select(Trend.keyword).where(Trend.source == "google_trends"))).scalars().all())
    articles = (await db.execute(select(Article))).scalars().all()
    removed = 0
    kept = 0
    for a in articles:
        if a.trend_keyword not in gt_keywords:
            await db.delete(a)
            removed += 1
        else:
            kept += 1
    await db.commit()
    return {"message": f"Removed {removed} legacy articles, kept {kept} real-trend articles"}


@router.post("/fix-images")
async def fix_article_images(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    import hashlib
    articles = (await db.execute(select(Article))).scalars().all()
    updated = 0
    seen_seeds = {}
    for a in articles:
        seed = hashlib.md5((a.title or a.trend_keyword or str(a.id)).encode()).hexdigest()[:8]
        base = f"https://picsum.photos/seed/{seed}/800/450"
        if base in seen_seeds:
            seed = hashlib.md5(f"{(a.title or a.trend_keyword or '')}-{a.id}".encode()).hexdigest()[:8]
            base = f"https://picsum.photos/seed/{seed}/800/450"
        seen_seeds[base] = a.id
        if a.image_url != base:
            a.image_url = base
            a.image_alt = f"Image illustrating {a.trend_keyword or a.title}"
            updated += 1
    await db.commit()
    return {"message": f"Updated {updated} article images"}


@router.post("/track")
async def track_event(
    event_type: str,
    article_id: int = None,
    page_url: str = None,
    referrer: str = None,
    user_agent: str = None,
    ip_address: str = None,
    country: str = None,
    duration_seconds: int = None,
    db: AsyncSession = Depends(get_db),
):
    await analytics.track_event(
        db, event_type,
        article_id=article_id,
        page_url=page_url,
        referrer=referrer,
        user_agent=user_agent,
        ip_address=ip_address,
        country=country,
        duration_seconds=duration_seconds,
    )
    return {"message": "Tracked"}
