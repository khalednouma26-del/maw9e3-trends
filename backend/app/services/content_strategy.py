import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger("maw9e3.strategy")

# High-value long-tail keyword patterns per niche
NICHE_KEYWORDS = {
    "health": {
        "angles": ["benefits", "risks", "symptoms", "treatment", "prevention", "causes", "remedies", "research"],
        "modifiers": ["natural", "effective", "proven", "clinical", "holistic", "dietary", "mental", "physical"],
        "audience": ["patients", "healthcare professionals", "caregivers", "fitness enthusiasts"],
        "question_stems": ["What causes", "How to treat", "Is it safe", "Can you prevent", "What are the symptoms of"],
    },
    "finance": {
        "angles": ["investing", "saving", "retirement", "tax", "budgeting", "real estate", "crypto", "stocks"],
        "modifiers": ["passive", "long-term", "low-risk", "high-yield", "diversified", "emergency", "smart", "strategic"],
        "audience": ["investors", "homeowners", "students", "retirees", "small business owners"],
        "question_stems": ["How much should I", "What is the best", "Is it worth", "When should I", "How does"],
    },
    "technology": {
        "angles": ["review", "comparison", "tutorial", "news", "security", "privacy", "automation", "development"],
        "modifiers": ["best", "affordable", "open-source", "cloud-based", "AI-powered", "user-friendly", "secure", "fastest"],
        "audience": ["developers", "IT professionals", "business owners", "gamers", "remote workers"],
        "question_stems": ["Which is better", "How to use", "What is the difference between", "Is it worth upgrading to", "How does"],
    },
    "sports": {
        "angles": ["training", "nutrition", "equipment", "strategies", "analysis", "predictions", "history", "records"],
        "modifiers": ["professional", "amateur", "competitive", "recreational", "elite", "youth", "indoor", "outdoor"],
        "audience": ["athletes", "coaches", "fans", "betting enthusiasts", "fitness trainers"],
        "question_stems": ["Who will win", "What is the best", "How to improve", "When is the next", "What are the rules of"],
    },
    "world": {
        "angles": ["analysis", "impact", "response", "history", "future", "policy", "security", "economy"],
        "modifiers": ["global", "international", "regional", "diplomatic", "strategic", "humanitarian", "economic", "political"],
        "audience": ["global citizens", "students", "professionals", "travelers", "policy makers"],
        "question_stems": ["What is happening in", "How does this affect", "Why is", "What caused", "What are the implications of"],
    },
    "politics": {
        "angles": ["policy", "election", "reform", "analysis", "debate", "legislation", "campaign", "governance"],
        "modifiers": ["bipartisan", "controversial", "progressive", "conservative", "federal", "state", "local", "international"],
        "audience": ["voters", "activists", "students", "policy makers", "journalists"],
        "question_stems": ["How will this policy", "What does this mean for", "Who supports", "Why did", "What are the arguments for"],
    },
    "entertainment": {
        "angles": ["review", "ranking", "news", "behind-the-scenes", "recommendations", "analysis", "history", "trends"],
        "modifiers": ["must-watch", "underrated", "classic", "award-winning", "binge-worthy", "critically-acclaimed", "fan-favorite", "hidden-gem"],
        "audience": ["movie buffs", "music lovers", "gamers", "streamers", "pop culture fans"],
        "question_stems": ["What to watch", "Is it worth", "Who is the best", "What are the best", "How does"],
    },
    "science": {
        "angles": ["discovery", "research", "breakthrough", "explanation", "study", "innovation", "theory", "experiment"],
        "modifiers": ["groundbreaking", "peer-reviewed", "theoretical", "applied", "experimental", "empirical", "cutting-edge", "interdisciplinary"],
        "audience": ["researchers", "students", "science enthusiasts", "educators", "curious minds"],
        "question_stems": ["What did scientists discover", "How does", "What is the science behind", "Is it true that", "Can we"],
    },
}

DEFAULT_ANGLES = ["overview", "analysis", "impact", "future", "guide"]
DEFAULT_MODIFIERS = ["important", "trending", "key", "notable", "significant"]
DEFAULT_AUDIENCE = ["readers", "professionals", "enthusiasts"]
DEFAULT_QUESTION_STEMS = ["What is", "Why is", "How does", "What are", "When did"]


class ContentStrategy:
    def get_focus_niches(self) -> list[str]:
        raw = settings.focus_niches
        if raw:
            return [n.strip().lower() for n in raw.split(",") if n.strip()]
        return []

    def is_focus_niche(self, category: str) -> bool:
        niches = self.get_focus_niches()
        if not niches:
            return True
        return category.lower() in niches

    def get_niche_data(self, category: str) -> dict:
        return NICHE_KEYWORDS.get(category, {
            "angles": DEFAULT_ANGLES,
            "modifiers": DEFAULT_MODIFIERS,
            "audience": DEFAULT_AUDIENCE,
            "question_stems": DEFAULT_QUESTION_STEMS,
        })

    def score_trend_for_niche(self, keyword: str, category: Optional[str]) -> int:
        niches = self.get_focus_niches()
        if not niches:
            return 0
        if category and category.lower() in niches:
            return 10
        kw_lower = keyword.lower()
        for niche in niches:
            data = NICHE_KEYWORDS.get(niche, {})
            for word_list in data.values():
                if any(w.lower() in kw_lower for w in word_list):
                    return 5
        return 0
