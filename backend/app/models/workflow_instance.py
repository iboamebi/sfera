"""
Workflow instance ORM model.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.workflow import Workflow


class WorkflowInstance(BaseModel):
    """Workflow execution instance."""

    __tablename__ = "workflow_instances"

    workflow_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflows.id"),
        nullable=False,
    )

    order_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("order_items.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="CREATED",
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    current_stage: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    workflow: Mapped[Workflow] = relationship()

    order_item: Mapped[OrderItem] = relationship()
