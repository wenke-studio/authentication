from pydantic import BaseModel


class AssetCreate(BaseModel):
    """Asset create schema

    Args:
        name (str): asset name
        uri (str, optional): asset uri. Defaults to None.
    """

    name: str
    uri: str | None = None

    class Config:
        from_attributes = True


class Asset(AssetCreate):
    """Asset schema

    Args:
        id (int): asset id
        name (str): asset name
        uri (str, optional): asset uri. Defaults to None.
    """

    id: int
