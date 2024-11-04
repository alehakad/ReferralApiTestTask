from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_async_session
from app.models import Referral
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.utils.jwt_utils import create_access_token, get_password_hash

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user: UserCreate, session: Annotated[AsyncSession, Depends(get_async_session)]):
    # check if user already exists
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.username, hashed_password=hashed_password)

    session.add(new_user)

    # add user to referral list
    if user.referral_code:
        referral_result = await session.execute(
            select(Referral)
            .options(selectinload(Referral.users))
            .where(Referral.referral_code == user.referral_code, Referral.is_active)
        )
        referral = referral_result.scalars().first()
        if referral:
            new_user.referrer_id = referral.referrer_id
            referral.users.append(new_user)

    await session.commit()
    await session.refresh(new_user)

    # create token
    access_token = create_access_token(data={"sub": new_user.username})
    return Token(access_token=access_token, token_type="bearer")
