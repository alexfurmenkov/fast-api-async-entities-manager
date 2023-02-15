from typing import AsyncGenerator

import pytest

from api.dependencies import get_users_manager, ensure_existing_user
from database.db_models import UserDBModel
from database.managers import UsersDBManager


@pytest.mark.asyncio
async def test_get_users_manager():
    """
    Unit test for get_users_manager dependency.
    """
    generator = get_users_manager()
    assert isinstance(generator, AsyncGenerator)
    manager: UsersDBManager = await anext(generator)
    assert isinstance(manager, UsersDBManager)


@pytest.mark.asyncio
async def test_ensure_existing_user(db_user: UserDBModel):
    user = await ensure_existing_user(db_user.id, await anext(get_users_manager()))
    assert user.id == db_user.id
