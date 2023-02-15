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
async def test_update_user(async_client: AsyncClient, db_user: UserDBModel):
    """
    Integration test for PUT /users/{user_id} endpoint.
    """
    request_body: dict = {
        "name": "new name",
        "age": 31,
    }

    # update a user
    update_response = await async_client.put(
        f"/users/{db_user.id}", data=json.dumps(request_body)
    )
    assert update_response.status_code == 200
    assert update_response.json() == {
        "message": f"User has been updated successfully",
        "user_id": db_user.id,
    }

    # get updated user and check that it has been updated
    get_response = await async_client.get(f"/users/{db_user.id}")
    get_response_body: dict = get_response.json()
    assert get_response_body["name"] == request_body["name"]
    assert get_response_body["age"] == request_body["age"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body, response_body",
    [
        (
            {},
            [
                {
                    "loc": ["body", "__root__"],
                    "msg": "one of username, name, surname or age must have a value",
                    "type": "value_error",
                }
            ],
        ),
        (
            {"name": ["test new name"]},
            [
                {
                    "loc": ["body", "name"],
                    "msg": "str type expected",
                    "type": "type_error.str",
                },
                {
                    "loc": ["body", "__root__"],
                    "msg": "one of username, name, surname or age must have a value",
                    "type": "value_error",
                },
            ],
        ),
    ],
)
async def test_update_user_invalid_body(
    async_client: AsyncClient,
    db_user: UserDBModel,
    request_body: dict,
    response_body: dict,
):
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when request body is invalid.
    """
    response = await async_client.put(
        f"/users/{db_user.id}", data=json.dumps(request_body)
    )
    assert response.status_code == 422
    assert response.json() == {"detail": response_body}


@pytest.mark.asyncio
async def test_update_user_not_found(async_client: AsyncClient):
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when requested user is not found.
    """
    user_id: str = str(uuid.uuid4())
    response = await async_client.put(f"/users/{user_id}", data=json.dumps({}))
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "User is not found",
            "user_id": user_id,
        }
    }


@pytest.mark.asyncio
async def test_update_user_username_exists(
    async_client: AsyncClient, db_user: UserDBModel, db_user_1: UserDBModel
):
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when a user with
    given username already exists.
    """
    request_body: dict = {
        "username": db_user_1.username,
    }
    response = await async_client.put(
        f"/users/{db_user.id}", data=json.dumps(request_body)
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "message": "Can't set username because it is occupied by another user",
            "username": request_body["username"],
        }
    }


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient):
    """
    Integration test for DELETE /users/{user_id} endpoint
    """
    # create a new user
    user_to_create: dict = {
        "username": "iivanov",
        "name": "Ivan",
        "surname": "Ivanov",
        "age": 33,
    }
    create_response = await async_client.post(
        "/users/", data=json.dumps(user_to_create)
    )

    # call the delete endpoint
    user_id: str = create_response.json()["new_user"]["id"]
    delete_response = await async_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "User has been deleted",
        "user_id": user_id,
    }


@pytest.mark.asyncio
async def test_delete_user_not_found(async_client: AsyncClient):
    """
    Integration test for DELETE /users/{user_id} endpoint.
    Checks the case when a user is not found.
    """
    user_id: str = str(uuid.uuid4())
    response = await async_client.delete(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "User is not found",
            "user_id": user_id,
        }
    }
