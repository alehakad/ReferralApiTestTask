from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    referrals = relationship("Referral", back_populates="referrer", cascade="all, delete-orphan")
    referral_used = relationship("Referral", secondary="user_referrals", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', referrer_id={self.referrer_id})>"
