from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from server.asset.models import asset_tag_relationship
from server.core.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    assets = relationship(
        "Asset",
        secondary=asset_tag_relationship,
        back_populates="tags",
        # lazy="dynamic",
    )
