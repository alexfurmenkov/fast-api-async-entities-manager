import json
import uuid

import pytest
from httpx import AsyncClient

from database.db_models import UserDBModel


@pytest.mark.asyncio
async def test_create_new_user(async_client: AsyncClient):
    """
    Integration test for POST /users endpoint
    """
    user_to_create: dict = {
        "username": "iivanov",
        "name": "Ivan",
        "surname": "Ivanov",
        "age": 33,
    }
    response = await async_client.post("/users/", data=json.dumps(user_to_create))

    # check response body
    assert response.status_code == 200
    response_body: dict = response.json()
    assert response_body["message"] == "User has been created successfully"

    new_user: dict = response_body["new_user"]
    assert new_user["id"]
    for key, value in user_to_create.items():
        assert new_user[key] == value

    # delete created user
    await async_client.delete(f"/users/{new_user['id']}")


@pytest.mark.asyncio
async def test_create_new_user_invalid_body(async_client: AsyncClient):
    """
    Integration test for POST /users endpoint.
    Checks the case when request body is invalid.
    """
    request_body: dict = {
        "username": "username",
        "name": "name",
        "surname": [{"key": "value"}],
    }
    response = await async_client.post("/users/", data=json.dumps(request_body))
    assert response.status_code == 422
    response_body: dict = response.json()
    assert response_body == {
        "detail": [
            {
                "loc": ["body", "surname"],
                "msg": "str type expected",
                "type": "type_error.str",
            }
        ]
    }


@pytest.mark.asyncio
async def test_create_new_user_username_exists(
    async_client: AsyncClient, db_user: UserDBModel
):
    """
    Integration test for POST /users endpoint.
    Checks the case when a user with
    given username already exists.
    """
    request_body: dict = {
        "username": db_user.username,
        "name": db_user.name,
        "surname": db_user.surname,
        "age": db_user.age,
    }
    response = await async_client.post("/users/", data=json.dumps(request_body))

    assert response.status_code == 400
    response_body: dict = response.json()
    assert response_body == {
        "detail": {
            "message": "User with given username already exists",
            "username": db_user.username,
        }
    }


@pytest.mark.asyncio
async def test_get_user_by_id(async_client: AsyncClient, db_user: UserDBModel):
    """
    Integration test for GET /users/{user_id} endpoint
    """
    response = await async_client.get(f"/users/{db_user.id}")
    assert response.status_code == 200
    response_body: dict = response.json()
    assert response_body == {
        "id": db_user.id,
        "username": db_user.username,
        "name": db_user.name,
        "surname": db_user.surname,
        "age": db_user.age,
    }


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(async_client: AsyncClient):
    """
    Integration test for GET /users/{user_id} endpoint.
    Checks the case when a user is not found.
    """
    user_id: str = str(uuid.uuid4())
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 404
    response_body: dict = response.json()
    assert response_body == {
        "detail": {
            "message": "User is not found",
            "user_id": user_id,
        }
    }


@pytest.mark.asyncio
async def test_update_user():
    """
    Integration test for PUT /users/{user_id} endpoint.
    """


@pytest.mark.asyncio
async def test_update_user_invalid_body():
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when request body is invalid.
    """


@pytest.mark.asyncio
async def test_update_user_not_found():
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when requested user is not found.
    """


@pytest.mark.asyncio
async def test_update_user_username_exists():
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when a user with
    given username already exists.
    """


@pytest.mark.asyncio
async def test_delete_user():
    """
    Integration test for DELETE /users/{user_id} endpoint
    """


@pytest.mark.asyncio
async def test_delete_user_not_found():
    """
    Integration test for DELETE /users/{user_id} endpoint.
    Checks the case when a user is not found.
    """
