import pytest
from faker import Faker
from pydantic import ValidationError

from server.asset import crud, schemas

faker = Faker()


def test_asset_create_schema():
    # case 1: uri is optional
    data = {"name": faker.name()}
    asset = schemas.AssetCreate(**data)
    assert asset

    # case 2: name is required
    with pytest.raises(ValidationError):
        data = {"uri": faker.uri()}
        asset = schemas.AssetCreate(**data)


def test_asset_update_schema():
    # case 1: uri is optional
    data = {"name": faker.name()}
    asset = schemas.AssetUpdate(**data)
    assert asset

    # case 2: name is optional
    data = {"uri": faker.name()}
    asset = schemas.AssetUpdate(**data)
    assert asset

    # case 3: check at least one field
    with pytest.raises(ValidationError):
        data = {}
        asset = schemas.AssetUpdate(**data)


def test_asset_model_schema(db):
    data = {"name": faker.name(), "uri": faker.uri()}
    asset = crud.create_asset(db, schemas.AssetCreate(**data))

    schema = schemas.Asset(**asset.__dict__)
    assert schema.id == asset.id
    assert schema.name == asset.name
    assert schema.uri == asset.uri
