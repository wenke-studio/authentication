from pydantic import BaseModel


class Tag(BaseModel):
    """Tag schema

    Args:
        id (int): tag id
        name (str): tag name
    """

    id: int
    name: str

    class Config:
        from_attributes = True
