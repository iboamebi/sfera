from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.device.value_objects.device_status import DeviceStatus


class DeviceCreate(BaseModel):
    instrument_type_id: UUID
    serial_number: str


class DeviceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    instrument_type_id: UUID
    serial_number: str
    status: DeviceStatus
