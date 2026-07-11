from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class VerificationMethod(BaseModel):
    __tablename__ = "verification_methods"

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
