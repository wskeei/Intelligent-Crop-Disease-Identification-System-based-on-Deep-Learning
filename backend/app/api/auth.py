from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token

router = APIRouter(prefix="/api/auth", tags=["用户认证"])

@router.post("/register", response_model=UserSchema)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """注册新用户"""
    # 检查用户名是否存在
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    
    # 创建用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/token", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """OAuth2 兼容的 token 登录接口"""
    # 查询用户
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    # 验证密码
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
