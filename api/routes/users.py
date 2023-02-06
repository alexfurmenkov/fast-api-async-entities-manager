from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from api.dependencies import ensure_existing_user, get_users_manager
from api.request_schemas import UserRequestSchema
from database.db_models import UserDBModel
from database.managers import UsersDBManager

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
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "User with given username already exists",
                "username": request_body.username,
            },
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
    try:
        await users_manager.update(user_id, **request_body.dict())
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Can't set username because it is occupied by another user",
                "username": request_body.username,
            },
        )
    return {"message": f"User with id {user_id} has been updated"}


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    users_manager: UsersDBManager = Depends(get_users_manager),
    existing_user: UserDBModel = Depends(ensure_existing_user),
) -> dict:
    await users_manager.delete(user_id)
    return {"message": f"User with id {user_id} has been deleted"}
