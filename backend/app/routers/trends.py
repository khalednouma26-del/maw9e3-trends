from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.trend import Trend
from app.services.trend_discovery import TrendDiscoveryService

router = APIRouter(prefix="/api/trends", tags=["trends"])
discovery = TrendDiscoveryService()


@router.get("")
async def list_trends(
    db: AsyncSession = Depends(get_db),
    q: str = Query(default="", description="Filter by keyword substring"),
    source: str = Query(default="", description="Filter by source"),
    limit: int = Query(default=100, ge=1, le=500),
):
    stmt = select(Trend).order_by(Trend.score.desc()).limit(limit)
    if q:
        stmt = select(Trend).where(Trend.keyword.ilike(f"%{q}%")).order_by(Trend.score.desc())
    if source:
        stmt = select(Trend).where(Trend.source == source).order_by(Trend.score.desc())
    result = await db.execute(stmt)
    trends = result.scalars().all()
    return [
        {
            "id": t.id,
            "keyword": t.keyword,
            "source": t.source,
            "score": t.score,
            "search_volume": t.search_volume,
            "category": t.category,
            "fetched_at": str(t.fetched_at),
        }
        for t in trends
    ]


@router.post("/refresh")
async def refresh_trends(db: AsyncSession = Depends(get_db)):
    trends = await discovery.discover_all()
    count = 0
    updated = 0
    from datetime import datetime
    for t in trends:
        existing = await db.execute(select(Trend).where(Trend.keyword == t["keyword"]))
        row = existing.scalar_one_or_none()
        if row is None:
            db.add(Trend(**t))
            count += 1
        else:
            for field in ("score", "search_volume", "category", "url", "seo_keywords"):
                if t.get(field) is not None:
                    setattr(row, field, t[field])
            row.fetched_at = datetime.utcnow()
            updated += 1
    await db.commit()
    return {"message": f"Fetched {len(trends)} trends, {count} new, {updated} updated", "total": len(trends), "new": count, "updated": updated}
