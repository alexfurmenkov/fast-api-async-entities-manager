from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import app_config
from database.db_models import UserDBModel
from database.managers import UsersDBManager

from ..users import get_users_manager


def create_access_token(user_id: str) -> str:
    """
    Generates JWT token.
    :param user_id: str
    :return: str
    """
    expires_delta = datetime.utcnow() + timedelta(
        minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_payload: dict = {"exp": expires_delta, "sub": str(user_id)}
    encoded_token = jwt.encode(
        token_payload, app_config.JWT_SECRET_KEY, app_config.JWT_ALGORITHM
    )
    return encoded_token


def create_refresh_token(user_id: str) -> str:
    """
    Generates refresh token.
    :param user_id: str
    :return: str
    """
    expires_delta = datetime.utcnow() + timedelta(
        minutes=app_config.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    token_payload: dict = {"exp": expires_delta, "sub": str(user_id)}
    encoded_token = jwt.encode(
        token_payload, app_config.JWT_SECRET_KEY, app_config.JWT_ALGORITHM
    )
    return encoded_token


def validate_token(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
) -> dict:
    """
    This function is supposed to be used as a dependency
    in the endpoints where unauthenticated access must be restricted.
    Decodes the JWT token and returns its payload.
    :param token: str
    :return: dict
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, app_config.JWT_SECRET_KEY, algorithms=[app_config.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload


async def get_current_user(
    token_payload: dict = Depends(validate_token),
    users_manager: UsersDBManager = Depends(get_users_manager),
) -> UserDBModel:
    """
    This function is supposed to be used as a dependency
    in the endpoints where we need to get current user.
    :param token_payload: dict
    :param users_manager: UsersDBManager
    :return: UserDBModel
    """
    user_id: str = token_payload.get("sub")
    user = await users_manager.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
