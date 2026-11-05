from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Customer(BaseModel):
    """ORM model for a customer contact."""

    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    contact_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    discount_percent: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
    )

    orders = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    sites = relationship(
        "Site",
        back_populates="customer",
    )
