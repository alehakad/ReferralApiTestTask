from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.models import Referral
from app.models.user import User
from app.utils.jwt_utils import create_access_token, get_password_hash, verify_password

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str
    referral_code: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=Token)
async def register(user: UserCreate, session: Annotated[AsyncSession, Depends(get_async_session)]):
    # check if user already exists
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # get referral code and referrer id
    referrer_id = None
    if user.referral_code:
        result = await session.execute(select(Referral).where(Referral.referral_code == user.referral_code,
                                                              Referral.is_active))
        referral = result.scalars().first()
        if referral:
            referrer_id = referral.referrer_id
    # create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, referrer_id=referrer_id)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # create token
    access_token = create_access_token(data={"sub": new_user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(user: UserCreate, session: Annotated[AsyncSession, Depends(get_async_session)]):
    # get user from db
    result = await session.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()

    # check password
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    # create token
    access_token = create_access_token({"sub": db_user.email})
    return Token(access_token=access_token, token_type="bearer")
