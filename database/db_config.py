import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


db_engine = create_async_engine(os.environ["DATABASE_URL"], future=True, echo=True)
async_db_session = sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
