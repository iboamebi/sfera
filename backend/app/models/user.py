import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
