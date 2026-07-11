from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.repair import RepairStatus


class RepairBase(BaseModel):
    order_item_id: UUID
    status: RepairStatus = RepairStatus.NEW
    description: str | None = None
    result: str | None = None


class RepairCreate(RepairBase):
    pass


class RepairUpdate(BaseModel):
    status: RepairStatus | None = None
    description: str | None = None
    result: str | None = None


class RepairRead(RepairBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
