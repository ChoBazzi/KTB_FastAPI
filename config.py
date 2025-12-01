from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MySQL 기본값 예시 (환경변수로 덮어씌울 수 있음)
    database_url: str = "mysql+pymysql://user:password@localhost:3306/ktb_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
