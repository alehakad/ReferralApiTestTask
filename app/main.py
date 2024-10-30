from fastapi import FastAPI
from app.db import init_db
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    #SessionLocal.remove()
