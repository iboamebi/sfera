"""
Workflow API schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.workflow.value_objects.workflow_status import (
    WorkflowStatus,
)


class WorkflowInstanceCreate(BaseModel):
    """Create workflow instance."""

    workflow_id: UUID
    order_item_id: UUID


class WorkflowMoveRequest(BaseModel):
    """Move workflow stage."""

    workflow_id: UUID


class WorkflowInstanceRead(BaseModel):
    """Workflow instance response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    workflow_id: UUID
    order_item_id: UUID
    current_stage: int
    status: WorkflowStatus
