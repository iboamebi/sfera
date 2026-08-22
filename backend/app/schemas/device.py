from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber


class DeviceCreate(BaseModel):
    instrument_type_id: UUID
    serial_number: str


class DeviceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    instrument_type_id: UUID
    serial_number: str
    status: DeviceStatus

    @field_validator("serial_number", mode="before")
    @classmethod
    def serialize_serial_number(cls, value: object) -> str:
        if isinstance(value, SerialNumber):
            return value.value
        return value
