import pytest
from faker import Faker

from server.conftest import TestingSessionLocal

from . import crud, models, schemas

faker = Faker()


@pytest.fixture
def asset_data():
    yield {"name": faker.name(), "uri": faker.uri()}


def test_create_asset(asset_data):
    db = TestingSessionLocal()
    asset = crud.create_asset(db, schemas.AssetCreate(**asset_data))

    assert isinstance(asset, models.Asset)
    assert asset.name == asset_data["name"]
    assert asset.uri == asset_data["uri"]

    record = db.query(models.Asset).filter(models.Asset.id == asset.id).one_or_none()
    assert record is not None


def test_retrieve_asset(asset_data):
    db = TestingSessionLocal()
    asset = crud.create_asset(db, schemas.AssetCreate(**asset_data))

    record = crud.retrieve_asset(db, asset.id)

    assert isinstance(record, models.Asset)
    assert record.name == asset_data["name"]
    assert record.uri == asset_data["uri"]
