import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.core.database import get_db
from server.core.schemas import HTTPError, HTTPSuccess

from . import controllers, schemas, tokens

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth/v1", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPSuccess,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Email Conflict",
            "model": HTTPError,
        },
    },
)
def register(credential: schemas.Credential, db: Session = Depends(get_db)):
    _, err = controllers.register_user(db, credential)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email has already been taken.",
        )
    return {"detail": "You have successfully registered."}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserToken,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "model": HTTPError,
        }
    },
)
def login(credential: schemas.Credential, db: Session = Depends(get_db)):
    user, err = controllers.authenticate_user(db, credential)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    user_token = tokens.create_token_by_user(user)
    return user_token
