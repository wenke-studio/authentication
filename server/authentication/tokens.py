from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from server.user.crud import get_user_by_email
from server.user.models import User

from .schemas import UserToken

# fixme: get secret key from environment variable
SECRET_KEY = "19f4169cdbfa57b2b47360d7b1a317705c29abc1ef8e7684b444de9a75bf0828"

ALGORITHM = "HS256"

DEFAULT_EXPIRE_MINUTES = 30


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
        return None, "invalid token"


def create_token_by_user(user: User) -> UserToken:
    access_token = encode({"email": user.email})
    refresh_token = encode({"email": user.email}, expires_delta=timedelta(days=1))
    return UserToken(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


def get_user_by_access_token(access_token: str, db: Session) -> tuple[User, None] | tuple[None, str]:
    payload, err = decode(access_token)
    if err:
        return None, "invalid token"
    user = get_user_by_email(db, payload.get("email"))
    if user is None:
        return None, "user not found"
    return user, None
