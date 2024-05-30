from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.core.database import get_db

from . import crud, schemas

router = APIRouter(
    prefix="/tag/v1",
    tags=["Tag"],
)


@router.get("/tag", response_model=list[schemas.Tag])
def list_tags(db: Session = Depends(get_db)):
    tags = crud.list_tags(db)
    return tags
