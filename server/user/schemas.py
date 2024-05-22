from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema for User

    Args:
        email (str): Email of the user
    """

    email: str


class UserCreate(UserBase):
    """Schema for creating a user

    Args:
        email (str): Email of the user
        password (str): Password of the user
    """

    password: str


class User(UserBase):
    """Schema for User

    Args:
        id (int): ID of the user
        email (str): Email of the user
    """

    id: int

    class Config:
        orm_mode = True
