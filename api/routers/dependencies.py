from fastapi import Depends, HTTPException

from database import async_db_session
from database.db_models import UserDBModel
from database.managers import UsersDBManager


async def get_users_manager() -> UsersDBManager:
    async with async_db_session() as session:
        async with session.begin():
            yield UsersDBManager(session)


async def ensure_existing_user(
    user_id: str, users_manager: UsersDBManager = Depends(get_users_manager)
):
    user: UserDBModel = await users_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} is not found"
        )
    return user
