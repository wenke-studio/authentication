import pytest
from faker import Faker

from server.conftest import TestingSessionLocal
from server.user.crud import check_password
from server.user.models import User

from . import tokens

faker = Faker()


@pytest.fixture
def user_data():
    return {"email": faker.email(), "password": faker.password()}


def test_register(http, user_data):
    # When we send a POST request to register a user
    response = http.post("/auth/v1/register", json=user_data)
    assert response.status_code == 201
    assert response.json()

    # Then the user should be in the database
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == user_data["email"]).one_or_none()
    assert user
    assert check_password(user, user_data["password"])


def test_login(http, user_data):
    # When a user is registered
    response = http.post("/auth/v1/register", json=user_data)
    assert response.status_code == 201

    # Then the user should be able to login
    response = http.post("/auth/v1/login", json=user_data)
    assert response.status_code == 200

    payload = response.json()
    assert tokens.decode(payload["access_token"])
    assert tokens.decode(payload["refresh_token"])
