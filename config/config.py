import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"])
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]
