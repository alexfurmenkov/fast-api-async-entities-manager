from fastapi import APIRouter, Depends

from database.db_models import UserDBModel
from database.managers import UsersDBManager
from request_schemas import UserRequestSchema
from routers.dependencies import get_users_manager

users_router = APIRouter(prefix="/users")


@users_router.post("/")
async def create_user(
    user: UserRequestSchema, users_manager: UsersDBManager = Depends(get_users_manager)
) -> dict:
    new_user: UserDBModel = await users_manager.create(
        user.username, user.name, user.surname, user.age
    )
    return {
        "message": "User has been created successfully",
        "user": new_user,
    }


@users_router.get("/{user_id}")
async def get_user(
    user_id: str, users_manager: UsersDBManager = Depends(get_users_manager)
) -> dict:
    user: UserDBModel = await users_manager.get(user_id)
    return user


@users_router.put("/{user_id}")
async def update_user(
    user_id: str,
    user: UserRequestSchema,
    users_manager: UsersDBManager = Depends(get_users_manager),
) -> dict:
    await users_manager.update(user_id, **user.dict())
    return {"message": f"User with id {user_id} has been updated"}


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: str, users_manager: UsersDBManager = Depends(get_users_manager)
) -> dict:
    await users_manager.delete(user_id)
    return {"message": f"User with id {user_id} has been deleted"}
