from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from server.core.database import Base

asset_tag_relationship = Table(
    "asset_tag_association",
    Base.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    uri = Column(String, nullable=True)

    tags = relationship(
        "Tag",
        secondary=asset_tag_relationship,
        back_populates="assets",
        lazy="dynamic",
    )
