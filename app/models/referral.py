from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.models.user import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referral_code = Column(String, unique=True, nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    referrer = relationship("User", back_populates="referrals")
