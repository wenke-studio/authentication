from faker import Faker
from sqlalchemy.orm import dynamic

from server.asset import models

faker = Faker()


def test_asset_model():
    asset = models.Asset(name=faker.name(), uri=faker.port_number())

    assert asset.name and asset.uri, "fields should exist"
    assert isinstance(asset.tags, dynamic.AppenderQuery)
