from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domains.device.value_objects.device_status import DeviceStatus
from app.domains.device.value_objects.serial_number import SerialNumber


class DeviceCreate(BaseModel):
    """Request for creating an instrument card."""

    instrument_type_id: UUID
    name: str
    serial_number: str


class DeviceUpdate(BaseModel):
    """Request for updating an instrument card."""

    name: str
    serial_number: str
    registry_number: str | None = None
    modification: str | None = None
    manufacture_year: int | None = Field(default=None, ge=1900, le=2100)
    inventory_number: str | None = None
    comment: str | None = None


class DeviceRead(BaseModel):
    """Response model for an instrument card."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    instrument_type_id: UUID
    name: str | None = None
    serial_number: str
    registry_number: str | None = None
    modification: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None
    status: DeviceStatus

    @field_validator("serial_number", mode="before")
    @classmethod
    def serialize_serial_number(cls, value: object) -> str:
        """Serialize the SerialNumber value object."""

        if isinstance(value, SerialNumber):
            return value.value
        return value
