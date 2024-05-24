from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

# ! fixme: Implement token encoding and decoding functions
# get a string like this: openssl rand -hex 32
SECRET_KEY = "19f4169cdbfa57b2b47360d7b1a317705c29abc1ef8e7684b444de9a75bf0828"

ALGORITHM = "HS256"

DEFAULT_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Union[str, None] = None


def encode(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode the data into a jwt token

    Args:
        data (dict): data to be encoded
        expires_delta (timedelta, optional): Expiry time for the token. Defaults is 30 mins.

    Returns:
        str: jwt token
    """

    # todo: does the data should be a user instance
    to_encode = data.copy()
    token_expires = expires_delta or timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    to_encode.update({"exp": datetime.now(timezone.utc) + token_expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode(token: str) -> tuple[dict, None] | tuple[None, str]:
    """Decode the token and return the payload if the token is valid

    Args:
        token (str): jwt token

    Returns:
        tuple[dict, None] | tuple[None, str]: payload, error
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload, None
    except InvalidTokenError:
        return None, "Invalid token"
