import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Site(BaseModel):
    """ORM model for an organization's service or operating site."""

    __tablename__ = "sites"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    organization = relationship(
        "Organization",
        back_populates="sites",
    )
