"""
Price list SQLAlchemy model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.price_list_item import PriceListItem


class PriceList(BaseModel):
    """SQLAlchemy model for price lists."""

    __tablename__ = "price_lists"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    price_list_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="GENERAL",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="RUB",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    valid_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    valid_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    items: Mapped[list[PriceListItem]] = relationship(
        back_populates="price_list",
        cascade="all, delete-orphan",
    )
