"""
Price list item model.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.price_list import PriceList


class PriceListItem(BaseModel):
    __tablename__ = "price_list_items"

    price_list_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("price_lists.id"),
        nullable=False,
    )

    service_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pcs",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price_list: Mapped[PriceList] = relationship(
        back_populates="items",
    )
