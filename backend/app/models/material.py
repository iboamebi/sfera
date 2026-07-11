from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Material(BaseModel):
    __tablename__ = "materials"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    article: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
