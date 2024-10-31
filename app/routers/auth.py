from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.models.user import User
from app.utils.jwt_utils import create_access_token, get_password_hash, verify_password

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()

    # check if user already exists
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # create token
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Annotated[AsyncSession, Depends(get_async_session)]):
    # get user from db
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()

    # check password
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # create token
    access_token = create_access_token({"sub": db_user.email})
    return Token(access_token=access_token, token_type="bearer")
