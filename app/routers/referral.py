from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session, get_current_user
from app.models import Referral
from app.models.user import User

router = APIRouter(dependencies=[Depends(get_current_user)])


class ReferralCreate(BaseModel):
    code: str
    expiration: datetime


@router.post("/referral/create")
async def create_referral(referral_data: ReferralCreate, user: Annotated[User, Depends(get_current_user)],
                          session: Annotated[AsyncSession, Depends(get_async_session)]):
    # check if user already created referral
    result = await session.execute(
        select(Referral).where(Referral.referrer_id == user.id, Referral.is_active))
    active_referral = result.scalars().first()

    if active_referral:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one referral code is allowed")

    # create new referral
    new_referral = Referral(referrer_id=user.id, code=referral_data.code, expiration=referral_data.expiration)

    session.add(new_referral)

    await session.commit()
    await session.refresh(new_referral)

    return {"message": "Referral code created successfully", "referral": new_referral.code}


@router.delete("/referral/delete")
async def delete_referral(user: Annotated[User, Depends(get_current_user)],
                          session: Annotated[AsyncSession, Depends(get_async_session)]):
    # check for active referral code
    result = await session.execute(
        select(Referral).where(Referral.referrer_id == user.id,
                               Referral.is_active)
    )
    active_referral = result.scalars().first()

    if not active_referral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active referral code found."
        )
    # delete the active user referral
    await session.delete(active_referral)
    await session.commit()

    return {"message": "Referral code deleted successfully"}


@router.get("/referral/info/{referrer_id}")
async def get_referrals_info(referrer_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    # get all user referrals
    result = await session.execute(select(Referral).where(Referral.referrer_id == referrer_id))
    referrals = result.scalars().all()

    if not referrals:
        return {"referrals": []}
    referral_info = [{"id": referral.id, "referral_code": referral.referral_code, "is_active": referral.is_active,
                      "created_at": referral.created_at} for referral in referrals]  # add users of referral


@router.get("/referral_code")
async def get_referral_code_by_email(email: str, session: Annotated[AsyncSession, Depends(get_async_session)]):
    # get user by email
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # find referral
    result = await session.execute(select(Referral).where(Referral.referrer_id == user.id, Referral.is_active))
    referral = result.scalars().first()

    if not referral:
        raise HTTPException(status_code=404, detail="No active referral code found for this user")

    return {"referral_code": referral.referral_code}
