from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    short_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    inn: Mapped[str | None] = mapped_column(
        String(12),
        nullable=True,
        unique=True,
    )

    kpp: Mapped[str | None] = mapped_column(
        String(9),
        nullable=True,
    )

    ogrn: Mapped[str | None] = mapped_column(
        String(15),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    customers = relationship(
        "Customer",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
