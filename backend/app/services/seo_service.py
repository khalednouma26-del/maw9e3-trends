from typing import Optional
from urllib.parse import urljoin

from app.config import settings


class SEOService:
    def generate_schema_article(self, article_data: dict) -> dict:
        return {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": article_data.get("meta_title", article_data.get("title", "")),
            "description": article_data.get("meta_description", ""),
            "image": article_data.get("image_url", ""),
            "author": {"@type": "Organization", "name": "Maw9e3 Trends", "url": settings.site_url},
            "publisher": {"@type": "Organization", "name": "Maw9e3 Trends", "url": settings.site_url},
            "datePublished": article_data.get("published_at", ""),
            "dateModified": article_data.get("updated_at", ""),
            "mainEntityOfPage": {"@type": "WebPage", "@id": urljoin(settings.site_url, f"/article/{article_data.get('id', '')}")},
            "keywords": article_data.get("tags", ""),
            "articleSection": article_data.get("category_name", "General"),
            "wordCount": article_data.get("word_count", 0),
        }

    def generate_breadcrumb_schema(self, items: list[dict]) -> dict:
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": item["name"], "item": item.get("item", settings.site_url)}
                for i, item in enumerate(items)
            ],
        }

    def generate_sitemap(self, articles: list[dict], pages: list[dict]) -> str:
        def url_entry(loc: str, freq: str, priority: float, lastmod: str = "", images: list[str] = None):
            parts = [f"  <url>", f"    <loc>{loc}</loc>", f"    <changefreq>{freq}</changefreq>", f"    <priority>{priority}</priority>"]
            if lastmod:
                parts.append(f"    <lastmod>{lastmod}</lastmod>")
            if images:
                for img in images:
                    parts.append(f"    <image:image><image:loc>{img}</image:loc></image:image>")
            parts.append("  </url>")
            return "\n".join(parts)

        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

        urls = [
            url_entry(f"{settings.site_url}/", "hourly", 1.0, now),
            url_entry(f"{settings.site_url}/trends", "hourly", 0.9, now),
            url_entry(f"{settings.site_url}/search", "daily", 0.8, now),
            url_entry(f"{settings.site_url}/about", "monthly", 0.5),
            url_entry(f"{settings.site_url}/contact", "monthly", 0.4),
        ]

        for a in articles:
            loc = f"{settings.site_url}/article/{a.get('id', '')}"
            lastmod = a.get("updated_at") or a.get("published_at") or ""
            imgs = [a["image_url"]] if a.get("image_url") else None
            urls.append(url_entry(loc, "weekly", 0.7, lastmod, imgs))

        for p in pages:
            urls.append(url_entry(f"{settings.site_url}/{p.get('slug', '')}", "monthly", 0.5))

        xmlns = ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.99"{xmlns}>
{''.join(urls)}
</urlset>"""

    def generate_robots_txt(self) -> str:
        return f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /dashboard/

Sitemap: {settings.site_url}/sitemap.xml
"""

    def get_og_tags(self, article: dict) -> dict:
        return {
            "og:title": article.get("meta_title", article.get("title", "")),
            "og:description": article.get("meta_description", ""),
            "og:image": article.get("image_url", ""),
            "og:type": "article",
            "og:url": urljoin(settings.site_url, f"/article/{article.get('id', '')}"),
            "og:site_name": "Maw9e3 Trends",
            "og:locale": "en_US",
        }

    def get_twitter_tags(self, article: dict) -> dict:
        return {
            "twitter:card": "summary_large_image",
            "twitter:title": article.get("meta_title", article.get("title", "")),
            "twitter:description": article.get("meta_description", ""),
            "twitter:image": article.get("image_url", ""),
            "twitter:site": "@maw9e3trends",
        }
