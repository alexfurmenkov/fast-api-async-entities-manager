import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from api.dependencies import get_users_manager
from app import app
from database.db_models import UserDBModel
from database.managers import UsersDBManager


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def db_user() -> UserDBModel:
    generator = get_users_manager()
    manager: UsersDBManager = await anext(generator)
    user: UserDBModel = await manager.create("username", "name", "surname", 32)

    yield user

    # create a new manager to start a new DB session
    new_generator = get_users_manager()
    new_manager: UsersDBManager = await anext(new_generator)
    await new_manager.delete(user.id)


@pytest_asyncio.fixture(scope="function")
async def db_user_1() -> UserDBModel:
    generator = get_users_manager()
    manager: UsersDBManager = await anext(generator)
    user: UserDBModel = await manager.create("new username", "new name", "new surname", 28)

    yield user

    # create a new manager to start a new DB session
    new_generator = get_users_manager()
    new_manager: UsersDBManager = await anext(new_generator)
    await new_manager.delete(user.id)
