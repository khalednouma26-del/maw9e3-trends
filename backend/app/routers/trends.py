from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.trend import Trend
from app.services.trend_discovery import TrendDiscoveryService

router = APIRouter(prefix="/api/trends", tags=["trends"])
discovery = TrendDiscoveryService()


@router.get("")
async def list_trends(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trend).order_by(Trend.score.desc()).limit(100))
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
    for t in trends:
        existing = await db.execute(select(Trend).where(Trend.keyword == t["keyword"]))
        if not existing.scalar_one_or_none():
            db.add(Trend(**t))
            count += 1
    await db.commit()
    return {"message": f"Fetched {len(trends)} trends, {count} new", "total": len(trends), "new": count}
