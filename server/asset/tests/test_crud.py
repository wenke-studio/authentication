import pytest
from faker import Faker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from server.asset import crud, models, schemas

faker = Faker()


def test_list_assets(db: Session):
    data = {"name": faker.name(), "uri": faker.uri()}
    crud.create_asset(db, schemas.AssetCreate(**data))

    assets = crud.list_assets(db)
    assert isinstance(assets, list)
    for asset in assets:
        assert isinstance(asset, models.Asset)


def test_create_asset(db: Session):
    data = {"name": faker.name()}  # `uri` is optional

    asset = crud.create_asset(db, schemas.AssetCreate(**data))
    assert isinstance(asset, models.Asset)
    assert asset.name == data["name"]
    assert asset.uri is None


def test_retrieve_asset(db: Session):
    data = {"name": faker.name(), "uri": faker.uri()}
    asset = crud.create_asset(db, schemas.AssetCreate(**data))

    retrieved_asset = crud.retrieve_asset(db, asset.id)
    assert isinstance(retrieved_asset, models.Asset)
    assert retrieved_asset.id == asset.id


def test_update_asset(db: Session):
    data = {"name": faker.name(), "uri": faker.uri()}
    asset = crud.create_asset(db, schemas.AssetCreate(**data))

    # case 1: `update_asset` should update the provided fields only.
    new_name = faker.name()
    affected_rows = crud.update_asset(db, asset.id, schemas.AssetUpdate(name=new_name))
    assert affected_rows == 1

    db.refresh(asset)
    assert asset.name == new_name
    assert asset.uri == data["uri"], "uri should not be updated when it is not provided"

    # case 2: `update_asset` should not update the None fields.
    new_uri = faker.uri()
    affected_rows = crud.update_asset(
        db,
        asset.id,
        schemas.AssetUpdate(name=None, uri=new_uri),
    )
    assert affected_rows == 1

    db.refresh(asset)
    assert asset.name == new_name, "name should not be updated"
    assert asset.uri == new_uri


def test_destroy_asset(db: Session):
    data = {"name": faker.name(), "uri": faker.uri()}
    asset = crud.create_asset(db, schemas.AssetCreate(**data))

    # case 1: `destroy_asset` should delete the asset and return success.
    affected_rows = crud.destroy_asset(db, asset.id)
    assert affected_rows == 1

    # case 2: `destroy_asset` should return failed if the asset is not found.
    with pytest.raises(NoResultFound):
        crud.destroy_asset(db, asset.id)
