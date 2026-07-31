import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.schemas.common import UserCreate, UserOut, TokenResponse
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

_login_attempts: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT = 10
_RATE_WINDOW = 300


def _check_rate_limit(key: str):
    now = time.time()
    window = _RATE_WINDOW
    _login_attempts[key] = [t for t in _login_attempts[key] if now - t < window]
    if len(_login_attempts[key]) >= _RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")
    _login_attempts[key].append(now)


@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    _check_rate_limit(f"register:{data.email}")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    existing = await db.execute(select(User).where((User.email == data.email) | (User.username == data.username)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email or username already exists")
    user = User(email=data.email, username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "User created", "user": UserOut.model_validate(user)}


@router.post("/login")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    _check_rate_limit(f"login:{request.client.host if request.client else 'unknown'}")
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)
