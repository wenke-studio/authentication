import pytest
from faker import Faker

from server.conftest import TestingSessionLocal

from .crud import check_password
from .models import User

faker = Faker()


@pytest.fixture
def user_data():
    yield {"email": faker.email(), "password": faker.password()}


def test_list_users(http, user_data):
    # Given a user in the database
    db = TestingSessionLocal()
    db.add(User(**user_data))
    db.commit()

    # Then the user should be returned in a list
    response = http.get("/user/v1/user")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "email": user_data["email"]}]


def test_create_user(http, user_data):
    # When a user is created
    response = http.post("/user/v1/user", json=user_data)
    assert response.status_code == 201

    # Then the user should be in the database
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == user_data["email"]).one_or_none()
    assert user


def test_retrieve_user(http, user_data):
    # Given a user in the database
    db = TestingSessionLocal()
    db.add(User(**user_data))
    db.commit()

    # Then the user should be returned in the response
    response = http.get("/user/v1/user/1")
    assert response.json() == {"id": 1, "email": user_data["email"]}


def test_update_user(http, user_data):
    # Given a user in the database
    db = TestingSessionLocal()
    db.add(User(**user_data))
    db.commit()

    new_password = faker.password()
    assert user_data["password"] != new_password

    # When the user is updated
    response = http.put("/user/v1/user/1", json={"password": new_password})
    assert response.status_code == 200, response.text

    # Then the user should be updated in the database
    user = db.query(User).filter(User.email == user_data["email"]).one_or_none()
    assert check_password(user, new_password)


def test_destroy_user(http, user_data):
    # Given a user in the database
    db = TestingSessionLocal()
    db.add(User(**user_data))
    db.commit()

    # When the user is deleted
    response = http.delete("/user/v1/user/1")
    assert response.status_code == 200

    # Then the user should be removed from the database
    user = db.query(User).filter(User.email == user_data["email"]).one_or_none()
    assert user is None
