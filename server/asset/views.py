from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.core.database import get_db

from . import crud, schemas

router = APIRouter(
    prefix="/asset/v1",
    tags=["Asset"],
)


@router.get("/asset", response_model=list[schemas.Asset])
def list_assets(db: Session = Depends(get_db)):
    assets = crud.list_assets(db)
    return assets
