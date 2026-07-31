from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class PageContent(BaseModel):
    slug: str
    title: str
    content: str
    meta_description: Optional[str] = None


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
