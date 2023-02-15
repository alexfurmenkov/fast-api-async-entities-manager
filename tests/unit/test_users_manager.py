import uuid
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.sql import Update, Delete

from database.db_models import UserDBModel
from database.managers import UsersDBManager


@pytest.mark.asyncio
async def test_create():
    session_mock = AsyncMock()
    manager = UsersDBManager(session_mock)

    username: str = "username"
    name: str = "name"
    surname: str = "surname"
    age: int = 25
    await manager.create(
        username, name, surname, age
    )

    user: UserDBModel = session_mock.add.call_args[0][0]
    assert user.username == username
    assert user.name == name
    assert user.surname == surname
    assert user.age == age

    session_mock.flush.assert_called()
    session_mock.commit.assert_called()


@pytest.mark.asyncio
async def test_get():
    session_mock = AsyncMock()
    manager = UsersDBManager(session_mock)

    user_id: str = str(uuid.uuid4())
    await manager.get(user_id)

    session_mock.get.assert_called_with(UserDBModel, user_id)


@pytest.mark.asyncio
async def test_update():
    session_mock = AsyncMock()
    manager = UsersDBManager(session_mock)

    user_id: str = str(uuid.uuid4())
    new_name: str = "new name"
    await manager.update(user_id, name=new_name)

    actual_call = session_mock.execute.call_args[0][0]
    assert isinstance(actual_call, Update)


@pytest.mark.asyncio
async def test_delete():
    session_mock = AsyncMock()
    manager = UsersDBManager(session_mock)

    user_id: str = str(uuid.uuid4())
    await manager.delete(user_id)

    actual_call = session_mock.execute.call_args[0][0]
    assert isinstance(actual_call, Delete)
