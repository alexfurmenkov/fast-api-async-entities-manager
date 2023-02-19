from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import (
    create_access_token,
    create_refresh_token,
    get_users_manager,
    PasswordManager
)
from api.request_schemas import CreateUserRequestSchema
from database.db_models import UserDBModel
from database.managers import UsersDBManager

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/signup")
async def create_user(
    request_body: CreateUserRequestSchema,
    users_manager: UsersDBManager = Depends(get_users_manager),
) -> dict:
    if await users_manager.find(username=request_body.username):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "User with given username already exists",
                "username": request_body.username,
            },
        )

    password_manager = PasswordManager(raw_password=request_body.password)
    new_user: UserDBModel = await users_manager.create(
        request_body.username,
        password_manager.hash_password(),
        request_body.name,
        request_body.surname,
        request_body.age,
    )
    return {
        "message": "User has been created successfully",
        "user_id": new_user.id,
    }


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_manager: UsersDBManager = Depends(get_users_manager),
) -> dict:
    users: List[UserDBModel] = await users_manager.find(username=form_data.username)
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email or password"
        )

    user = users[0]  # we assume that only one user can exist with the same username
    password_manager = PasswordManager(raw_password=form_data.password)
    if not password_manager.verify_password(hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
