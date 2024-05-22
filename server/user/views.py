from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.core.schemas import HTTPError
from server.dependencies import get_db

from . import controller, schemas

router = APIRouter(prefix="/user/v1", tags=["User"])


@router.post("/user", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = controller.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return controller.create_user(db=db, user=user)


@router.get("/user", status_code=200)
def list_users(db: Session = Depends(get_db)):
    return controller.get_users(db)


@router.get(
    "/user/{user_id}",
    response_model=schemas.User,
    status_code=200,
    responses={
        404: {
            "description": "User not found",
            "model": HTTPError,
        }
    },
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controller.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
