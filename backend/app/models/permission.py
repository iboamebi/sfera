from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Permission(BaseModel):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
