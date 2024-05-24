import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.core.schemas import HTTPError, HTTPSuccess
from server.dependencies import get_db

from . import controllers, schemas, token

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
    response_model=schemas.Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "model": HTTPError,
        }
    },
)
def login(credential: schemas.Credential, db: Session = Depends(get_db)):
    user, err = controllers.login(db, credential)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = token.encode({"email": user.email})
    refresh_token = token.encode({"email": user.email}, expires_delta=timedelta(days=1))
    return {
        "user": {"id": user.id, "email": user.email},
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
