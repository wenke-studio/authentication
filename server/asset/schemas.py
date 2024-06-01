from __future__ import annotations

from pydantic import BaseModel, model_validator


class AssetCreate(BaseModel):
    """Asset create schema

    Args:
        name (str): asset name
        uri (str, optional): asset uri. Defaults to None.
    """

    name: str
    uri: str | None = None


class AssetUpdate(BaseModel):
    """Asset update schema

    Args:
        name (str, optional): asset name. Defaults to None.
        uri (str, optional): asset uri. Defaults to None.
    """

    name: str | None = None
    uri: str | None = None

    @model_validator(mode="after")
    def check_at_least_one(self) -> AssetUpdate:
        conditions = [self.name is None, self.uri is None]
        if all(conditions):
            raise ValueError("At least one field is required, `name` or `uri`")
        return self


class Asset(BaseModel):
    """Asset schema

    Args:
        id (int): asset id
        name (str): asset name
        uri (str, optional): asset uri. Defaults to None.
    """

    id: int
    name: str
    uri: str | None = None

    class Config:
        from_attributes = True
