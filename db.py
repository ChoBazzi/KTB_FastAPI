from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings


def _get_connect_args(url: str):
    # SQLite는 단일 스레드 체크를 끄는 옵션이 필요하다.
    return {"check_same_thread": False} if url.startswith("sqlite") else {}


SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=_get_connect_args(SQLALCHEMY_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
