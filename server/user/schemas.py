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


class UserUpdate(BaseModel):
    """Schema for updating a user

    Args:
        password (str): Password of the user
    """

    password: str | None


class User(UserBase):
    """Schema for User

    Args:
        id (int): ID of the user
        email (str): Email of the user
    """

    id: int

    class Config:
        from_attributes = True
