from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Methodology(BaseModel):
    __tablename__ = "methodologies"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    document_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
