import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Site(BaseModel):
    """ORM model for a customer's service or operating site."""

    __tablename__ = "sites"

    __table_args__ = (
        UniqueConstraint("id", "customer_id", name="uq_sites_id_customer_id"),
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("customers.id"),
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

    customer = relationship(
        "Customer",
        back_populates="sites",
    )

    orders = relationship(
        "Order",
        back_populates="site",
    )

    instruments = relationship(
        "Instrument",
        back_populates="site",
    )
