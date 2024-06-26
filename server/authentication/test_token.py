import pytest
from faker import Faker

from . import tokens

faker = Faker()


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "email": faker.email(),
    }


def test_encode(user_data):
    access_token = tokens.encode(user_data)
    assert access_token and isinstance(access_token, str)


def test_decode(user_data):
    access_token = tokens.encode(user_data)

    payload, err = tokens.decode(access_token)
    assert err is None
    assert payload and isinstance(payload, dict)
