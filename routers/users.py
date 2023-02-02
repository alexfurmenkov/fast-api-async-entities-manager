import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from database.db_models import UserDBModel
from database.managers import UsersDBManager
from request_schemas import UserRequestSchema
from routers.dependencies import get_users_manager, ensure_existing_user

users_router = APIRouter(prefix="/users")


@users_router.post("/")
async def create_user(
    request_body: UserRequestSchema,
    users_manager: UsersDBManager = Depends(get_users_manager),
) -> dict:
    try:
        new_user: UserDBModel = await users_manager.create(
            request_body.username,
            request_body.name,
            request_body.surname,
            request_body.age,
        )
    except IntegrityError as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail=f"User with username {request_body.username} already exists",
        )
    return {
        "message": "User has been created successfully",
        "new_user": new_user,
    }


@users_router.get("/{user_id}")
async def get_user(
    user_id: str, user: UserDBModel = Depends(ensure_existing_user)
) -> dict:
    return user


@users_router.put("/{user_id}")
async def update_user(
    user_id: str,
    request_body: UserRequestSchema,
    users_manager: UsersDBManager = Depends(get_users_manager),
    existing_user: UserDBModel = Depends(ensure_existing_user),
) -> dict:
    await users_manager.update(user_id, **request_body.dict())
    return {"message": f"User with id {user_id} has been updated"}


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    users_manager: UsersDBManager = Depends(get_users_manager),
    existing_user: UserDBModel = Depends(ensure_existing_user),
) -> dict:
    await users_manager.delete(user_id)
    return {"message": f"User with id {user_id} has been deleted"}
