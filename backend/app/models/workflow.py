"""
Workflow ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.workflow_stage import WorkflowStage


class Workflow(BaseModel):
    """Workflow database model."""

    __tablename__ = "workflows"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    stages: Mapped[list[WorkflowStage]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
    )
