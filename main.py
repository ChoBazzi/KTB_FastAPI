from fastapi import FastAPI
import logging

from db import Base, engine
from router.post_router import router as post_router
from router.user_router import router as user_router

logging.basicConfig(level=logging.INFO)

# SQLite 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
    








