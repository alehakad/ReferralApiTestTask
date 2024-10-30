import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.user import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/referral_db")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
