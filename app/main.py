from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import get_async_session, init_db
from app.models import User
from app.routers import auth, referral
from app.schemas.token import Token
from app.utils.jwt_utils import create_access_token, verify_password


# create db models on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(referral.router, prefix="/referral")


@app.post("/token")
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[AsyncSession, Depends(get_async_session)]) -> Token:
    # get user from db
    result = await session.execute(select(User).where(User.username == user_data.username))
    db_user = result.scalars().first()

    # check password
    if not db_user or not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    # create token
    access_token = create_access_token({"sub": db_user.username})
    return Token(access_token=access_token, token_type="bearer")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
