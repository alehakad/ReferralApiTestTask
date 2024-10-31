from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func, CheckConstraint, UniqueConstraint
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

    # only one active code for user
    __table_args__ = (
        CheckConstraint('expiration_date > NOW()', name='check_expiration_date_future'),
        UniqueConstraint('referrer_id', name='unique_active_referral_per_user',
                         postgresql_where="expiration_date > NOW()")
    )

    # check if referral is active
    @hybrid_property
    def is_active(self):
        return self.expiration_date > func.now()

    @is_active.expression
    def is_active(cls):
        return cls.expiration_date > func.now()
