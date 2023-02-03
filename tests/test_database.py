from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from api.routes.dependencies import get_users_manager
from app import app
from config import app_config
from database.managers import UsersDBManager

# create a session for test database
engine = create_async_engine(app_config.DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def override_get_users_manager() -> UsersDBManager:
    """
    Overrides get_users_manager dependency
    to connect to test database.
    :return: UsersDBManager
    """
    async with TestingSessionLocal() as session:
        async with session.begin():
            yield UsersDBManager(session)


# override app dependencies
app.dependency_overrides[get_users_manager] = override_get_users_manager
