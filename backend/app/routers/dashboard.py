from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.models.user import User
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
