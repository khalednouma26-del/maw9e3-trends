import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.database import init_db
from app.routers import trends, articles, pages, auth, dashboard, pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("maw9e3")

scheduler = AsyncIOScheduler()


async def scheduled_trends():
    from app.database import async_session
    from app.services.trend_discovery import TrendDiscoveryService
    td = TrendDiscoveryService()
    async with async_session() as db:
        try:
            trends = await td.discover_all()
            for t in trends:
                from sqlalchemy import select
                from app.models.trend import Trend
                existing = await db.execute(select(Trend).where(Trend.keyword == t["keyword"]))
                if not existing.scalar_one_or_none():
                    db.add(Trend(**t))
            await db.commit()
            logger.info("Scheduled trend discovery: %d trends", len(trends))
        except Exception as e:
            logger.error("Scheduled trend discovery error: %s", e)


async def scheduled_content():
    from app.database import async_session
    from app.services.auto_publisher import AutoPublisher
    publisher = AutoPublisher()
    async with async_session() as db:
        try:
            result = await publisher.run_full_pipeline(db)
            logger.info("Scheduled content pipeline: %s", result)
        except Exception as e:
            logger.error("Scheduled content pipeline error: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler.add_job(scheduled_trends, "interval", hours=settings.trends_refresh_interval_hours, id="trends", replace_existing=True)
    scheduler.add_job(scheduled_content, "interval", hours=settings.content_gen_interval_hours, id="content", replace_existing=True)
    scheduler.start()
    logger.info("Scheduler started")
    yield
    scheduler.shutdown()


origins = [settings.site_url] if settings.site_url != "*" else ["*"]
app = FastAPI(title="Maw9e3 Trends API", version="2.0.0", lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trends.router)
app.include_router(articles.router)
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(pipeline.router)


@app.get("/")
async def root():
    return {
        "name": "Maw9e3 Trends",
        "version": "2.0.0",
        "endpoints": {
            "trends": "/api/trends/",
            "articles": "/api/articles/",
            "sitemap": "/api/sitemap.xml",
            "robots": "/robots.txt",
            "auth": "/api/auth/",
            "dashboard": "/api/dashboard/stats",
            "pipeline": "/api/pipeline/",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
