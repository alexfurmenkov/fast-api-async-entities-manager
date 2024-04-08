import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 43800))  # one month
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
