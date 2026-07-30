"""
Repair API schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.repair.value_objects.repair_status import (
    RepairStatus,
)


class RepairCreate(BaseModel):
    """Create repair request."""

    order_item_id: UUID
    description: str | None = None


class RepairComplete(BaseModel):
    """Complete repair request."""

    result: str


class RepairRead(BaseModel):
    """Repair response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    order_item_id: UUID
    status: RepairStatus
    description: str | None = None
    result: str | None = None
