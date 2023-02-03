import json


def test_create_new_user(client):
    """
    Integration test for POST /users endpoint
    """
    user_to_create: dict = {
        "username": "iivanov",
        "name": "Ivan",
        "surname": "Ivanov",
        "age": 33
    }
    response = client.post("/users", data=json.dumps(user_to_create))

    # check response body
    assert response.status_code == 200
    response_body: dict = response.json()
    assert response_body["message"] == "User has been created successfully"

    new_user: dict = response_body["new_user"]
    assert new_user["id"]
    for key, value in user_to_create.items():
        assert new_user[key] == value

    # delete created user
    client.delete(f"/users/{new_user['id']}")


def test_create_new_user_invalid_body():
    """
    Integration test for POST /users endpoint.
    Checks the case when request body is invalid.
    """


def test_create_new_user_username_exists():
    """
    Integration test for POST /users endpoint.
    Checks the case when a user with
    given username already exists.
    """


def test_get_user_by_id():
    """
    Integration test for GET /users/{user_id} endpoint
    """


def test_get_user_by_id_not_found():
    """
    Integration test for GET /users/{user_id} endpoint.
    Checks the case when a user is not found.
    """


def test_update_user():
    """
    Integration test for PUT /users/{user_id} endpoint.
    """


def test_update_user_invalid_body():
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when request body is invalid.
    """


def test_update_user_username_exists():
    """
    Integration test for PUT /users/{user_id} endpoint.
    Checks the case when a user with
    given username already exists.
    """


def test_delete_user():
    """
    Integration test for DELETE /users/{user_id} endpoint
    """


def test_delete_user_not_found():
    """
    Integration test for DELETE /users/{user_id} endpoint.
    Checks the case when a user is not found.
    """
