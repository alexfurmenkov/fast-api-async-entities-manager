from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from api.dependencies import ensure_existing_user, get_users_manager, validate_token
from api.request_schemas import UpdateUserRequestSchema
from database.db_models import UserDBModel
from database.managers import UsersDBManager

users_router = APIRouter(prefix="/users", dependencies=[Depends(validate_token)])


@users_router.get("/{user_id}")
async def get_user(
    user_id: str,
    existing_user: UserDBModel = Depends(ensure_existing_user),
) -> dict:
    return existing_user


@users_router.put("/{user_id}")
async def update_user(
    user_id: str,
    request_body: UpdateUserRequestSchema,
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
    return {
        "message": f"User has been updated successfully",
        "user_id": user_id,
    }


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    users_manager: UsersDBManager = Depends(get_users_manager),
    existing_user: UserDBModel = Depends(ensure_existing_user),
) -> dict:
    await users_manager.delete(user_id)
    return {
        "message": "User has been deleted",
        "user_id": user_id,
    }
