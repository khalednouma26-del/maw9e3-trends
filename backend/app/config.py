import os
from pydantic_settings import BaseSettings


import secrets


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./maw9e3.db"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = secrets.token_urlsafe(32)
    openai_api_key: str = ""
    gemini_api_key: str = ""
    site_url: str = "http://localhost:3000"
    admin_email: str = "admin@maw9e3.com"
    focus_niches: str = ""  # Comma-separated: e.g. "health,finance,technology"
    trends_refresh_interval_hours: int = 1
    content_gen_interval_hours: int = 2
    update_interval_hours: int = 24

    class Config:
        env_file = ".env"


settings = Settings()
