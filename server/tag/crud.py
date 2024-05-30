from sqlalchemy.orm import Session

from .models import Tag


def list_tags(db: Session):
    return db.query(Tag).all()
