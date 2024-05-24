import pytest
from faker import Faker

from server.authentication import tokens
from server.user.crud import create_user
from server.user.schemas import UserCreate

from .conftest import TestingSessionLocal

faker = Faker()


@pytest.fixture
def user_data():
    yield {"email": faker.email(), "password": faker.password()}


def test_token(http, user_data):
    db = TestingSessionLocal()
    create_user(db, UserCreate(**user_data))

    response = http.post(
        "/token",
        data={
            "username": user_data["email"],  # use email as username
            "password": user_data["password"],
        },
    )
    assert response.status_code == 200

    payload = response.json()
    assert tokens.decode(payload["access_token"])
    assert tokens.decode(payload["refresh_token"])
