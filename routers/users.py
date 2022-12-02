from fastapi import APIRouter

from database import async_db_session
from database.db_models import UserDBModel
from database.managers import UsersDBManager
from request_schemas import UserRequestSchema


users_router = APIRouter(prefix="/users")


@users_router.post("/")
async def create_user(user: UserRequestSchema):
    async with async_db_session() as session:
        async with session.begin():
            users_manager = UsersDBManager(session)
            new_user: UserDBModel = await users_manager.create(user.username, user.name, user.surname, user.age)

    return {"message": f"User with id {new_user.id} has been created"}


@users_router.get("/{user_id}")
async def get_user(user_id: str) -> dict:
    async with async_db_session() as session:
        async with session.begin():
            users_manager = UsersDBManager(session)
            user: UserDBModel = await users_manager.get(user_id)

    return {"user": user}


@users_router.put("/{user_id}")
async def update_user(user_id: str, user: UserRequestSchema):
    async with async_db_session() as session:
        async with session.begin():
            users_manager = UsersDBManager(session)
            await users_manager.update(**user.dict())

    return {"message": f"User with id {user_id} has been updated"}


@users_router.delete("/{user_id}")
async def delete_user(user_id: str):
    async with async_db_session() as session:
        async with session.begin():
            users_manager = UsersDBManager(session)
            await users_manager.delete(user_id)

    return {"message": f"User with id {user_id} has been deleted"}
