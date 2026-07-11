from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Warehouse(BaseModel):
    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    responsible_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
