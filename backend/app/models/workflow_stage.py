"""
Workflow stage ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.workflow import Workflow


class WorkflowStage(BaseModel):
    """Workflow stage database model."""

    __tablename__ = "workflow_stages"

    workflow_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflows.id"),
        nullable=False,
    )

    order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    performer_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    required: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    workflow: Mapped[Workflow] = relationship(
        back_populates="stages",
    )
