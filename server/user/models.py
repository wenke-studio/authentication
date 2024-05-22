from __future__ import annotations

import logging

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Session

from server.core.database import Base

from . import schemas

logger = logging.getLogger(__name__)


def make_password(password: str) -> str:
    # fixme: use a proper hashing algorithm
    return password + "notreallyhashed"


def check_password(user: schemas.User, password: str) -> bool:
    return user.password == make_password(password)


class Manager:
    def list(self, db: Session):
        return db.query(User).all()

    def create(self, db: Session, user: schemas.UserCreate):
        user = User(email=user.email, password=make_password(user.password))
        db.add(user)
        db.commit()
        return user

    def retrieve(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).one()

    def update(self, db: Session, user_id: int, password: str):
        affected_rows = db.query(User).filter(User.id == user_id).update({"password": make_password(password)})
        db.commit()
        return affected_rows

    def destroy(self, db: Session, user_id: int):
        affected_rows = db.query(User).filter(User.id == user_id).delete()
        db.commit()
        return affected_rows

    def get_by_email(self, db: Session, email: str):
        stmt = select(User.id).where(User.email == email)
        user = db.execute(stmt).one()
        return user[0]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    objects = Manager()
