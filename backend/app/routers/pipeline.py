from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.auto_publisher import AutoPublisher

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])
publisher = AutoPublisher()


@router.post("/run")
async def run_pipeline(db: AsyncSession = Depends(get_db)):
    result = await publisher.run_full_pipeline(db)
    return {"message": "Pipeline executed", **result}


@router.get("/status")
async def pipeline_status():
    return {"status": "active"}
