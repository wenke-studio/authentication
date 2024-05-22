import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from server.core.schemas import HTTPError, HTTPSuccess
from server.dependencies import get_db

from . import schemas
from .models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user/v1", tags=["User"])


@router.get("/user", response_model=list[schemas.User], status_code=200)
def list_users(db: Session = Depends(get_db)):
    users = User.objects.list(db)
    return users


@router.post(
    "/user",
    response_model=schemas.User,
    status_code=201,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Email Conflict",
            "model": HTTPError,
        }
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = User.objects.create(db, user)
        return user
    except IntegrityError as exc:
        logger.error(exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email has already been taken.",
        )


@router.get(
    "/user/{user_id}",
    response_model=schemas.User,
    status_code=200,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
            "model": HTTPError,
        }
    },
)
def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = User.objects.retrieve(db, user_id)
        return user
    except NoResultFound as exc:
        logger.error(exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )


@router.put(
    "/user/{user_id}",
    status_code=200,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
            "model": HTTPError,
        }
    },
)
def update_user(user_id: int, password: str, db: Session = Depends(get_db)):
    affected_rows = User.objects.update(db, user_id, password)
    if affected_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return {"detail": "success"}


@router.delete(
    "/user/{user_id}",
    status_code=200,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
            "model": HTTPError,
        }
    },
)
def destroy_user(user_id: int, db: Session = Depends(get_db)):
    affected_rows = User.objects.destroy(db, user_id)
    if affected_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return {"detail": "success"}
