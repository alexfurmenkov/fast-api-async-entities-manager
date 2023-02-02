import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
