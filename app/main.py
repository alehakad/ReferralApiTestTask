from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # SessionLocal.remove()
