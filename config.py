from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 로컬 실행은 별도 DB 설치 없이 SQLite로 동작하고, 배포 환경에서는
    # DATABASE_URL 환경변수로 MySQL/PostgreSQL 등을 주입한다.
    database_url: str = "sqlite:///./ktb_app.db"
    model_path: str = "resnet50_food.h5"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
