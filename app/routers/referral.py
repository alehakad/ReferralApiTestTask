from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_async_session
from app.dependencies import User, get_current_user
from app.models import Referral
from app.schemas.referral import ReferralCreate

router = APIRouter(tags=["referrals"])


@router.post("/create")
async def create_referral(
        referral_data: ReferralCreate,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        # check if user already created referral
        result = await session.execute(
            select(Referral).where(Referral.referrer_id == user.id, Referral.is_active)
        )
        active_referral = result.scalars().first()

        if active_referral:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Only one active referral code is allowed")

        # create new referral
        new_referral = Referral(referrer_id=user.id, referral_code=referral_data.code,
                                expiration_date=referral_data.expiration)

        session.add(new_referral)
        await session.commit()
        await session.refresh(new_referral)

        return {"message": "Referral code created successfully", "referral": new_referral.referral_code}

    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Duplicate referral keys or wrong expiration date")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete")
async def delete_referral(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        # check for active referral code
        result = await session.execute(
            select(Referral).where(Referral.referrer_id == user.id, Referral.is_active)
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

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/info/{referrer_id}")
async def get_referrals_info(
        referrer_id: int,
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        # get all user referrals
        result = await session.execute(
            select(Referral)
            .options(selectinload(Referral.users))
            .where(Referral.referrer_id == referrer_id)
        )
        referrals = result.scalars().all()

        if not referrals:
            return {"referrals": []}

        referral_info = []
        for referral in referrals:
            referral_info.append({
                "id": referral.id,
                "referral_code": referral.referral_code,
                "is_active": referral.is_active,
                "created_at": referral.created_at,
                "users_referred": [
                    {
                        "id": user.id,
                        "email": user.email
                    }
                    for user in referral.users
                ]
            })

        return referral_info

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/referral_code")
async def get_referral_code_by_email(
        email: str,
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        # get user by email
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # find referral
        result = await session.execute(select(Referral).where(Referral.referrer_id == user.id, Referral.is_active))
        referral = result.scalars().first()

        if not referral:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No active referral code found for this user")

        return {"referral_code": referral.referral_code}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
