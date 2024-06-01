from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from . import models, schemas


def list_assets(db: Session) -> list[models.Asset]:
    """Return a list of all assets in the database

    Args:
        db (Session): SQLAlchemy session

    Returns:
        list[models.Asset]: List of all assets in the database

    Raises:
        SQLAlchemyError: If there is an error in the database
    """
    return db.query(models.Asset).all()


def create_asset(db: Session, asset_create: schemas.AssetCreate) -> models.Asset:
    """Create an asset

    Args:
        db (Session): SQLAlchemy session
        asset_create (schemas.AssetCreate): Asset data to create

    Returns:
        models.Asset: The created asset

    Raises:
        SQLAlchemyError: If there is an error in the database
    """
    data = asset_create.model_dump(exclude_none=True)
    asset = models.Asset(**data)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def retrieve_asset(db: Session, asset_id: int) -> models.Asset:
    """Retrieve an asset

    Args:
        db (Session): SQLAlchemy session
        asset_id (int): Asset ID

    Returns:
        models.Asset: The asset found with the ID

    Raises:
        NoResultFound: If no asset is found with the ID
        MultipleResultsFound: If more than one asset is found with the ID
    """
    result = db.query(models.Asset).filter(models.Asset.id == asset_id)
    return result.one()


def update_asset(db: Session, asset_id: int, asset_update: schemas.AssetUpdate) -> int:
    """Update an asset

    Args:
        db (Session): SQLAlchemy session
        asset_id (int): Asset ID
        asset_update (schemas.AssetUpdate): Asset data to update

    Returns:
        int: Number of affected rows

    Raises:
        NoResultFound: If no asset is found with the ID
    """
    affected_rows = (
        db.query(models.Asset)
        .filter(models.Asset.id == asset_id)
        .update(
            asset_update.model_dump(exclude_none=True),
        )
    )
    if affected_rows == 0:
        raise NoResultFound(f"No asset found with id `{asset_id}`")
    db.commit()
    return affected_rows


def destroy_asset(db: Session, asset_id: int) -> int:
    """Delete an asset

    Args:
        db (Session): SQLAlchemy session
        asset_id (int): Asset ID

    Returns:
        int: Number of affected rows

    Raises:
        NoResultFound: If no asset is found with the ID
    """
    affected_rows = db.query(models.Asset).filter(models.Asset.id == asset_id).delete()
    if affected_rows == 0:
        raise NoResultFound(f"No asset found with id `{asset_id}`")
    db.commit()
    return affected_rows
