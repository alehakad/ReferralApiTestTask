from datetime import datetime
from typing import List

from pydantic import BaseModel


class ReferralCreate(BaseModel):
    code: str
    expiration: datetime


class UserReferred(BaseModel):
    id: int
    email: str


class ReferralInfo(BaseModel):
    id: int
    referral_code: str
    is_active: bool
    created_at: datetime
    users_referred: List[UserReferred] = []
