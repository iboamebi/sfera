from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


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

    items: Mapped[list["PriceListItem"]] = relationship(
        back_populates="price_list",
        cascade="all, delete-orphan",
    )
