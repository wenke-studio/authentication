import pytest
from django.contrib.auth.hashers import check_password

from user.models import User


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser",
    }


@pytest.fixture
def create_user(user_data):
    def _create_user():
        return User.objects.create_user(**user_data)

    return _create_user


def test_create_user(create_user, user_data):
    user = create_user()
    assert user.email == user_data["email"]
    assert check_password(user_data["password"], user.password)
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active


def test_create_superuser(create_user, user_data):
    user_data["is_staff"] = True
    user_data["is_superuser"] = True
    user = create_user()
    assert user.email == user_data["email"]
    assert check_password(user_data["password"], user.password)
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active


def test_str_method(create_user, user_data):
    user = create_user()
    assert str(user) == user_data["username"]


def test_username_default(create_user, user_data):
    user_data.pop("username")
    user = create_user()
    assert user.username is None
