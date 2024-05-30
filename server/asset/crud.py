from sqlalchemy.orm import Session

from . import models, schemas


def create_asset(db: Session, asset: schemas.AssetCreate):
    asset = models.Asset(name=asset.name, uri=asset.uri)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def retrieve_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).one_or_none()
