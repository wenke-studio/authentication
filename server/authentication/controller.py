import logging

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from server.user.models import User, check_password

from .schemas import Credential

logger = logging.getLogger(__name__)

ReturnType = tuple[User | None, str | None]


def register_user(db: Session, credential: Credential) -> ReturnType:
    try:
        user = User.objects.create(db, credential)
        return user, None
    except IntegrityError as exc:
        logger.error("error creating user, %s", str(exc))
        return None, "The email has already been taken."


def login(db: Session, credential: Credential) -> ReturnType:
    try:
        user = User.objects.get_by_email(db, credential.email)
        if not check_password(user, credential.password):
            return None, "invalid password"
        return user, None
    except NoResultFound as exc:
        logger.error("error logging in, %s", str(exc))
        return None, "Invalid credentials."
