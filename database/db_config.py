from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import app_config

load_dotenv()


db_engine = create_async_engine(app_config.DATABASE_URL, future=True, echo=True)
async_db_session = sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession, autoflush=True)
