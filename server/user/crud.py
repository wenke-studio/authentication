import logging

from sqlalchemy.orm import Session

from . import schemas
from .models import User

logger = logging.getLogger(__name__)


def make_password(password: str) -> str:
    # fixme: use a proper hashing algorithm
    return password + "notreallyhashed"


def check_password(user: schemas.User, password: str) -> bool:
    return user.password == make_password(password)


def get_user_by_email(db: Session, email: str) -> User:
    return db.Query(User).filter(User.email == email).first()


def list_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: schemas.UserCreate):
    user = User(email=user.email, password=make_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def retrieve_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one()


def update_user(db: Session, user_id: int, password: str):
    affected_rows = (
        db.query(User)
        .filter(User.id == user_id)
        .update(
            {"password": make_password(password)},
        )
    )
    db.commit()
    return affected_rows


def destroy_user(db: Session, user_id: int):
    affected_rows = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return affected_rows
