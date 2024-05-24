import hashlib
import logging

from sqlalchemy.orm import Session

from . import schemas
from .models import User

logger = logging.getLogger(__name__)

# fixme: get salt from environment variable
SALT = b".\x8a\xb0\xf5\xe3N\xdd\n\x1dD\xf1\xe4\x99\xc8\x87\xb6"

HASH_ARGS = {"n": 2**14, "r": 8, "p": 1}


def get_password_hash(password: str) -> str:
    hashed_password = hashlib.scrypt(password.encode("utf-8"), salt=SALT, **HASH_ARGS)
    return hashed_password.hex()


def verify_password(user: schemas.User, password: str) -> bool:
    return user.password == get_password_hash(password)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).one_or_none()


def list_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(db: Session, user: schemas.UserCreate) -> User:
    user = User(email=user.email, password=get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def retrieve_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).one_or_none()


def update_user(db: Session, user_id: int, password: str) -> int:
    affected_rows = (
        db.query(User)
        .filter(User.id == user_id)
        .update(
            {"password": get_password_hash(password)},
        )
    )
    db.commit()
    return affected_rows


def destroy_user(db: Session, user_id: int) -> int:
    affected_rows = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return affected_rows
