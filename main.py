from fastapi import FastAPI
import logging

from db import Base, engine
from router.post_router import router as post_router
from router.user_router import router as user_router
from router.predict_router import router as predict_router
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

# mysql 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(predict_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 특정 도메인 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # <-- OPTIONS 허용
    allow_headers=["*"],
)





