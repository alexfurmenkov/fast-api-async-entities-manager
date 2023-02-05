import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from api.routes.dependencies import get_users_manager
from app import app
from database.db_models import UserDBModel
from database.managers import UsersDBManager


@pytest.yield_fixture(scope='session')
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
async def db_user(request) -> UserDBModel:
    gen = get_users_manager()
    manager: UsersDBManager = await anext(gen)
    user: UserDBModel = await manager.create("username", "name", "surname", 32)

    async def cleanup():  # TODO fix finalizer
        await manager.delete(user.id)
    request.addfinalizer(cleanup)

    return user
