import pytest
from django.contrib.auth.hashers import check_password
from faker import Faker

from user.models import User

faker = Faker()


@pytest.fixture
def user_data():
    return {
        "email": faker.email(),
        "password": faker.password(),
        "username": faker.user_name(),
    }


@pytest.mark.django_db
def test_create_user(user_data):
    user = User.objects.create_user(**user_data)
    assert user.email == user_data["email"]
    assert check_password(user_data["password"], user.password)
    assert not user.is_staff
    assert not user.is_superuser
    assert not user.is_active, "User should not be active by default"


@pytest.mark.django_db
def test_create_superuser(user_data):
    user = User.objects.create_superuser(**user_data)
    assert user.email == user_data["email"]
    assert check_password(user_data["password"], user.password)
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_str_method(user_data):
    user = User.objects.create_user(**user_data)
    assert str(user) == user_data["username"]


@pytest.mark.django_db
def test_username_default(user_data):
    user_data.pop("username")
    user = User.objects.create_user(**user_data)
    assert user.username == ""
    assert str(user) == user_data["email"]
