"""
Price list model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.price_list_item import PriceListItem


class PriceList(BaseModel):
    __tablename__ = "price_lists"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
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
