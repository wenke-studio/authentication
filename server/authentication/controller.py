import logging

from sqlalchemy.orm import Session

from server.user import controller
from server.user.models import User

from .schemas import Credential

logger = logging.getLogger(__name__)

ReturnType = tuple[User | None, str | None]


def register_user(db: Session, credential: Credential) -> ReturnType:
    user = controller.get_user_by_email(db, email=credential.email)
    if user:
        logger.error("duplicate email, email=%s", credential.email)
        return None, "duplicate email"
    user = controller.create_user(db, user=credential)
    return user, None


def login(db: Session, credential: Credential) -> ReturnType:
    user = controller.get_user_by_email(db, email=credential.email)
    if not user:
        logger.error("user not found, email=%s", credential.email)
        return None, "user not found"
    if not controller.check_password(user, password=credential.password):
        logger.error("invalid password, password=%s", credential.password)
        return None, "invalid password"
    return user, None
