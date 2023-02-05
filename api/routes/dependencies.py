from typing import AsyncGenerator

from fastapi import Depends, HTTPException

from database import async_db_session
from database.db_models import UserDBModel
from database.managers import UsersDBManager


async def get_users_manager() -> AsyncGenerator:
    """
    Yields an instance of UsersDBManager.
    :return: AsyncGenerator
    """
    async with async_db_session() as session:
        async with session.begin():
            yield UsersDBManager(session)


async def ensure_existing_user(
    user_id: str, users_manager: UsersDBManager = Depends(get_users_manager)
):
    """
    Checks that the users exists in the database.
    Returns HTTP 400 response if not.
    :param user_id: str
    :param users_manager: UsersDBManager
    :return: None
    """
    user: UserDBModel = await users_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} is not found"
        )
    return user
