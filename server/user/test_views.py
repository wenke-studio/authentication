import pytest
from faker import Faker

from server.authentication.tokens import create_token_by_user
from server.conftest import TestingSessionLocal

from .crud import create_user, get_user_by_email, verify_password
from .schemas import UserCreate

faker = Faker()


@pytest.fixture
def user_data():
    yield {"email": faker.email(), "password": faker.password()}


def create_a_new_user(user_data):
    db = TestingSessionLocal()
    user = create_user(
        db,
        UserCreate(email=user_data["email"], password=user_data["password"]),
    )
    return user


@pytest.fixture
def admin_access_token():
    admin = create_a_new_user({"email": faker.email(), "password": faker.password()})
    token = create_token_by_user(admin)
    return token.access_token


def test_list_users(http, admin_access_token):
    # Then the user should be returned in the response
    response = http.get(
        "/user/v1/user",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 1
    assert "id" in payload[0]
    assert "email" in payload[0]
    assert "password" not in payload[0]


def test_create_user(http, user_data, admin_access_token):
    # When a new user is created
    response = http.post(
        "/user/v1/user",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 201

    # Then the user should be in the database
    db = TestingSessionLocal()
    user = get_user_by_email(db, user_data["email"])
    assert user


def test_retrieve_user(http, user_data, admin_access_token):
    # Given a user in the database
    user = create_a_new_user(user_data)

    # Then the user should be returned in the response
    response = http.get(
        f"/user/v1/user/{user.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert user.id == payload["id"]
    assert user.email == payload["email"]
    assert "password" not in payload


def test_update_user(http, user_data, admin_access_token):
    # Given a user in the database
    user = create_a_new_user(user_data)

    new_password = faker.password()
    assert user_data["password"] != new_password

    # When the user password is updated
    response = http.put(
        f"/user/v1/user/{user.id}",
        json={"password": new_password},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200, response.text

    # Then the user should be updated in the database
    db = TestingSessionLocal()
    refreshed_user = get_user_by_email(db, user_data["email"])
    assert verify_password(refreshed_user, new_password)


def test_destroy_user(http, user_data, admin_access_token):
    # Given a user in the database
    user = create_a_new_user(user_data)

    # When the user is deleted
    response = http.delete(
        f"/user/v1/user/{user.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200

    # Then the user should be removed from the database
    db = TestingSessionLocal()
    deleted_user = get_user_by_email(db, user_data["email"])
    assert deleted_user is None
