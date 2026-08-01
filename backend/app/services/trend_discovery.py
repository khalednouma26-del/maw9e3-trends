import asyncio
import logging
import math
import re
import feedparser
import httpx
from datetime import datetime, timezone
from typing import Optional

from app.config import settings

logger = logging.getLogger("maw9e3.trends")


CATEGORY_FEEDS = {
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://www.theguardian.com/world/rss",
    ],
    "politics": [
        "https://feeds.bbci.co.uk/news/politics/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "https://www.politico.com/rss/politics.xml",
    ],
    "sports": [
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.espn.com/espn/rss/news",
        "https://sports.yahoo.com/rss",
    ],
    "finance": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    ],
    "health": [
        "https://feeds.bbci.co.uk/news/health/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        "https://www.who.int/feeds/entity/emergencies/diseases/en/rss.xml",
    ],
    "entertainment": [
        "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",
        "https://variety.com/feed/",
    ],
    "science": [
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "https://www.nationalgeographic.com/rss",
    ],
    "technology": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    ],
}


JUNK_KEYWORDS = {
    "try searching to get started", "home", "playback", "keyboard shortcuts", "history",
    "search", "watch", "settings", "sign in", "get youtube", "report history", "help",
    "about", "press", "copyright", "contact us", "creators", "advertise", "developers",
    "terms", "privacy", "policy", "safety", "how youtube works", "test new features",
    "nfl sunday ticket", "trending now", "explore", "live", "music", "gaming",
    "sports", "films", "podcasts", "library", "library history", "shorts",
    "subscriptions", "your channel", "yt music", "youtube premium", "google llc",
    "welcome back", "you're offline", "check your connection",
}


class TrendDiscoveryService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)

    async def close(self):
        await self.client.aclose()

    def _parse_traffic(self, raw) -> Optional[int]:
        if not raw:
            return None
        m = re.match(r"([\d.]+)\s*(k|m|b)?\+?", str(raw).strip().lower())
        if not m:
            return None
        n = float(m.group(1))
        mult = {"k": 1e3, "m": 1e6, "b": 1e9}.get(m.group(2) or "", 1)
        return int(n * mult)

    def _traffic_score(self, vol) -> float:
        if not vol:
            return 70.0
        return round(min(100.0, 60 + 10 * math.log10(vol)), 1)

    async def from_google_trends(self) -> list[dict]:
        try:
            url = "https://trends.google.com/trending/rss?geo=US"
            resp = await self.client.get(url)
            feed = feedparser.parse(resp.text)
            trends = []
            seen = set()
            for entry in feed.entries[:40]:
                keyword = entry.get("title", "").strip()
                if not keyword or keyword in seen:
                    continue
                seen.add(keyword)
                traffic = self._parse_traffic(entry.get("ht_approx_traffic"))
                news_title = entry.get("ht_news_item_title", "") or ""
                news_url = entry.get("ht_news_item_url", "") or ""
                trends.append({
                    "keyword": keyword,
                    "source": "google_trends",
                    "score": self._traffic_score(traffic),
                    "search_volume": traffic,
                    "category": self._guess_category(f"{keyword} {news_title}"),
                    "url": news_url,
                    "seo_keywords": news_title or None,
                })
            return trends
        except Exception as e:
            logger.warning("Google Trends error: %s", e)
            return []

    async def from_google_news(self) -> list[dict]:
        try:
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            resp = await self.client.get(url)
            feed = feedparser.parse(resp.text)
            trends = []
            seen = set()
            for entry in feed.entries[:30]:
                title = entry.get("title", "").strip()
                if title and title not in seen:
                    seen.add(title)
                    trends.append({
                        "keyword": title,
                        "source": "google_news",
                        "score": round(95 - len(trends) * 2, 1),
                        "search_volume": None,
                        "url": entry.get("link", ""),
                        "category": self._guess_category(title),
                    })
            return trends
        except Exception as e:
            logger.warning("Google News error: %s", e)
            return []

    async def from_category_rss(self) -> list[dict]:
        trends = []
        seen = set()
        for cat, urls in CATEGORY_FEEDS.items():
            for url in urls:
                try:
                    resp = await self.client.get(url)
                    feed = feedparser.parse(resp.text)
                    for entry in feed.entries[:8]:
                        title = entry.get("title", "").strip()
                        if title and title not in seen:
                            seen.add(title)
                            trends.append({
                                "keyword": title,
                                "source": f"rss_{cat}",
                                "score": round(85 - len(trends) * 1.5, 1),
                                "search_volume": None,
                                "url": entry.get("link", ""),
                                "category": cat,
                            })
                except Exception as e:
                    logger.warning("RSS error for %s/%s: %s", cat, url, e)
        return trends

    async def from_reddit(self) -> list[dict]:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; TrendDiscovery/1.0)"}
            subreddits = ["worldnews", "politics", "sports", "finance", "health", "entertainment", "science", "technology"]
            trends = []
            seen = set()
            for sub in subreddits:
                try:
                    resp = await self.client.get(f"https://www.reddit.com/r/{sub}/hot/.json?limit=10", headers=headers)
                    data = resp.json()
                    for post in data.get("data", {}).get("children", []):
                        d = post.get("data", {})
                        title = d.get("title", "").strip()
                        if title and title not in seen:
                            seen.add(title)
                            trends.append({
                                "keyword": title,
                                "source": "reddit",
                                "score": round(min(d.get("ups", 0) / 100, 100), 1),
                                "search_volume": d.get("ups", 0),
                                "url": f"https://reddit.com{d.get('permalink', '')}",
                                "category": "politics" if sub == "politics" else ("world" if sub == "worldnews" else sub),
                            })
                except Exception:
                    continue
            return trends
        except Exception as e:
            logger.warning("Reddit error: %s", e)
            return []

    async def from_youtube(self) -> list[dict]:
        try:
            url = "https://www.youtube.com/feed/trending?hl=en&gl=US"
            resp = await self.client.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            trends = []
            seen = set()
            for script in soup.find_all("script"):
                if "var ytInitialData" in script.text:
                    import re
                    matches = re.findall(r'"title":\s*\{\s*"runs":\s*\[\s*\{\s*"text":\s*"([^"]+)"', script.text)
                    for m in matches:
                        if m and m not in seen:
                            seen.add(m)
                            trends.append({
                                "keyword": m,
                                "source": "youtube",
                                "score": round(85 - len(trends) * 3, 1),
                                "search_volume": None,
                                "category": self._guess_category(m),
                            })
                    break
            return trends[:20]
        except Exception as e:
            logger.warning("YouTube error: %s", e)
            return []

    async def from_twitter(self) -> list[dict]:
        try:
            resp = await self.client.get("https://trends24.in/united-states")
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            trends = []
            seen = set()
            for item in soup.select("a.trend-link")[:30]:
                text = item.get_text(strip=True)
                if text and text not in seen:
                    seen.add(text)
                    trends.append({
                        "keyword": text,
                        "source": "twitter",
                        "score": round(80 - len(trends) * 2, 1),
                        "search_volume": None,
                        "category": self._guess_category(text),
                    })
            return trends
        except Exception as e:
            logger.warning("Twitter error: %s", e)
            return []

    def _guess_category(self, keyword: str) -> str:
        kw = keyword.lower()
        sports_keywords = ["sport", "game", "match", "championship", "nfl", "nba", "mlb", "nhl",
                          "soccer", "football", "basketball", "tennis", "f1", "olympic", "ufc",
                          "world cup", "league", "player", "coach", "stadium", "goal", "score",
                          "united", "madrid", "barcelona", "liverpool", "chelsea", "arsenal",
                          "golf", "cricket", "debut", "tournament", "title fight", "gp ", "circuit",
                          "quarterfinal", "semifinal", "playoff", "pitch", "mvp", "race"]
        finance_keywords = ["stock", "market", "bitcoin", "crypto", "bank", "invest", "economy",
                           "inflation", "recession", "gdp", "trade", "tariff", "dollar", "fed",
                           "interest rate", "bond", "etf", "nasdaq", "s&p", "dow jones"]
        politics_keywords = ["politics", "election", "president", "congress", "senate", "vote", "democrat",
                            "republican", "government", "policy", "law", "bill", "parliament", "minister",
                            "campaign", "political", "trump", "biden", "ukraine", "russia", "china", "war",
                            "sanction", "diplomat", "foreign", "nato", "united nations"]
        health_keywords = ["health", "covid", "disease", "vaccine", "hospital", "doctor", "drug",
                           "medical", "patient", "cancer", "virus", "mental health", "fda",
                           "salmonella", "recall", "outbreak", "hospitalized", "infection",
                           "ebola", "flu", "obesity", "diet", "fitness", "workout", "wellness"]
        entertainment_keywords = ["movie", "film", "music", "celebrity", "netflix", "show", "actor",
                                 "actress", "song", "album", "concert", "award", "oscar", "grammy",
                                 "hollywood", "disney", "marvel", "trailer", "series"]
        science_keywords = ["science", "space", "nasa", "climate", "research", "study", "discover",
                           "dinosaur", "planet", "mars", "moon", "evolution", "gene", "dna"]
        tech_keywords = ["ai", "artificial intelligence", "robot", "software", "app", "iphone",
                        "android", "microsoft", "google", "apple", "meta", "facebook", "instagram",
                        "tiktok", "chatgpt", "gpt", "quantum", "cyber", "data"]

        for cat, words in [
            ("sports", sports_keywords), ("finance", finance_keywords),
            ("politics", politics_keywords), ("health", health_keywords),
            ("entertainment", entertainment_keywords), ("science", science_keywords),
            ("technology", tech_keywords),
        ]:
            if any(w in kw for w in words):
                return cat
        return "general"

    async def discover_all(self) -> list[dict]:
        sources = [
            self.from_google_trends(),
            self.from_google_news(),
            self.from_category_rss(),
            self.from_reddit(),
            self.from_youtube(),
            self.from_twitter(),
        ]
        results = await asyncio.gather(*sources, return_exceptions=True)
        all_trends = []
        for r in results:
            if isinstance(r, list):
                all_trends.extend(r)
        return self._deduplicate(all_trends)

    def _deduplicate(self, trends: list[dict]) -> list[dict]:
        seen = set()
        deduped = []
        for t in trends:
            kw = t["keyword"].strip().lower()
            if not kw or kw in seen or kw in JUNK_KEYWORDS:
                continue
            if len(kw) < 3:
                continue
            seen.add(kw)
            deduped.append(t)
        return deduped
