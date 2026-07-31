import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.page import Page
from app.models.contact import ContactMessage
from app.schemas.common import PageContent, ContactForm

logger = logging.getLogger("maw9e3.pages")
router = APIRouter(tags=["pages"])


@router.get("/api/pages/{slug}")
async def get_page(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).where(Page.slug == slug))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"id": page.id, "slug": page.slug, "title": page.title, "content": page.content, "meta_description": page.meta_description}


@router.post("/api/contact")
async def contact_form(form: ContactForm, db: AsyncSession = Depends(get_db)):
    msg = ContactMessage(name=form.name, email=form.email, subject=form.subject, message=form.message)
    db.add(msg)
    await db.commit()
    logger.info("Contact message from %s: %s", form.email, form.subject)
    return {"message": "Thank you for your message. We will get back to you soon."}


@router.get("/api/sitemap.xml")
async def sitemap(db: AsyncSession = Depends(get_db)):
    from fastapi.responses import Response
    from app.services.seo_service import SEOService
    seo = SEOService()
    result = await db.execute(select(Page))
    pages = result.scalars().all()
    result = await db.execute(
        select(__import__("app.models.article", fromlist=["Article"]).Article)
        .where(__import__("app.models.article", fromlist=["Article"]).Article.published == 1)
    )
    articles = result.scalars().all()
    article_list = [{"id": a.id} for a in articles]
    page_list = [{"slug": p.slug} for p in pages]
    xml = seo.generate_sitemap(article_list, page_list)
    return Response(content=xml, media_type="application/xml")


@router.get("/robots.txt")
async def robots():
    from fastapi.responses import Response
    from app.services.seo_service import SEOService
    seo = SEOService()
    return Response(content=seo.generate_robots_txt(), media_type="text/plain")
