from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .base import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referral_code = Column(String, unique=True, nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    referrer = relationship("User", back_populates="referrals")
    users = relationship("User", secondary="user_referrals", back_populates="referral_used")

    __table_args__ = (
        CheckConstraint("expiration_date > created_at", name="check_expiration_date_future"),
    )

    # check if referral is active
    @hybrid_property
    def is_active(self):
        return self.expiration_date > datetime.now(timezone.utc)

    @is_active.expression
    def is_active(cls):
        return cls.expiration_date > func.now()


class UserReferral(Base):
    __tablename__ = 'user_referrals'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    referral_id = Column(Integer, ForeignKey('referrals.id'), primary_key=True)
