from datetime import datetime

from pydantic import BaseModel


class ReferralCreate(BaseModel):
    code: str
    expiration: datetime
