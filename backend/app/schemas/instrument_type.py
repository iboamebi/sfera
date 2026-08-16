from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InstrumentTypeBase(BaseModel):
    name: str
    manufacturer: str | None = None
    model: str | None = None
    measurement_type: str | None = None
    accuracy_class: str | None = None
    verification_interval_months: int | None = None
    description: str | None = None


class InstrumentTypeCreate(InstrumentTypeBase):
    pass


class InstrumentTypeUpdate(BaseModel):
    name: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    measurement_type: str | None = None
    accuracy_class: str | None = None
    verification_interval_months: int | None = None
    description: str | None = None


class InstrumentTypeRead(InstrumentTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
