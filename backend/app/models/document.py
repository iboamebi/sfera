import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Document(BaseModel):
    __tablename__ = "documents"

    order_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("orders.id"),
        nullable=True,
    )

    document_template_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("document_templates.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
