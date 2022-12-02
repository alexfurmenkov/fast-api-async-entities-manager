from fastapi import APIRouter

from request_schemas import UserRequestSchema
from services.database import read_item, save_item, delete_item


users_router = APIRouter(prefix="/users")


@users_router.post("/")
async def create_user(user: UserRequestSchema):
    save_item(user.dict())
    return {"message": f"User with id {user.id} has been created"}


@users_router.get("/{user_id}")
async def get_user(user_id: str) -> dict:
    user: dict = read_item(user_id)
    return {"user": user}


@users_router.put("/{user_id}")
async def update_user(user_id: str, user: UserRequestSchema):
    save_item(user.dict())
    return {"message": f"User with id {user_id} has been updated"}


@users_router.delete("/{user_id}")
async def delete_user(user_id: str):
    delete_item(user_id)
    return {"message": f"User with id {user_id} has been deleted"}
