import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from server.core.database import get_db
from server.core.schemas import HTTPError, HTTPSuccess

from . import crud, schemas

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/asset/v1",
    tags=["Asset"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Asset],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        }
    },
)
def list_assets(db: Session = Depends(get_db)):
    try:
        assets = crud.list_assets(db)
        return assets
    except SQLAlchemyError as exc:
        logging.error("Error creating asset: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating asset",
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Asset,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        }
    },
)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
):
    try:
        asset = crud.create_asset(db, asset)
        return asset
    except SQLAlchemyError as exc:
        logging.error("Error creating asset: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating asset",
        )


@router.get(
    "/{asset_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Asset,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Asset Not Found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def retrieve_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        asset = crud.retrieve_asset(db, asset_id)
        return asset
    except NoResultFound as exc:
        logging.error("Asset not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    except SQLAlchemyError as exc:
        # include MultipleResultsFound
        logging.error("Error retrieving asset: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving asset",
        )


@router.put(
    "/{asset_id}",
    status_code=status.HTTP_200_OK,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Asset Not Found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def update_asset(
    asset_id: int,
    asset: schemas.AssetUpdate,
    db: Session = Depends(get_db),
):
    try:
        asset = crud.update_asset(db, asset_id, asset)
        return {"detail": "Asset updated"}
    except NoResultFound as exc:
        logging.error("Asset not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    except SQLAlchemyError as exc:
        logging.error("Error updating asset: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating asset",
        )


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_200_OK,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Asset Not Found",
            "model": HTTPError,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "DB Error",
            "model": HTTPError,
        },
    },
)
def destroy_asset(asset_id: int, db: Session = Depends(get_db)):
    try:
        crud.destroy_asset(db, asset_id)
        return {"detail": "Asset deleted"}
    except NoResultFound as exc:
        logging.error("Asset not found: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    except SQLAlchemyError as exc:
        logging.error("Error deleting asset: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting asset",
        )
