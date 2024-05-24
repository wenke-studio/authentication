import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.user import crud
from server.user.models import User

from .schemas import Credential

logger = logging.getLogger(__name__)

ReturnType = tuple[User, None] | tuple[None, str]


def register_user(db: Session, credential: Credential) -> ReturnType:
    try:
        user = crud.create_user(db, credential)
        return user, None
    except IntegrityError as exc:
        logger.error("error creating user, %s", str(exc))
        return None, "email conflict"


def authenticate_user(db: Session, credential: Credential) -> ReturnType:
    user = crud.get_user_by_email(db, credential.email)
    if not user:
        return None, "user not found"
    is_valid = crud.verify_password(user, credential.password)
    if not is_valid:
        return user, "invalid password"
    return user, None
