from pydantic import BaseModel

from server.user.schemas import User, UserCreate


class Credential(UserCreate):
    """Credential schema

    same as UserCreate schema

    Args:
        email (str): email
        password (str): password
    """

    pass


class Token(BaseModel):
    """Token schema

    Args:
        user (User): includes id and email
        access_token (str): access token
        refresh_token (str): refresh token
    """

    user: User
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True
