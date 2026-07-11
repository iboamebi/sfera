from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    organization_id: UUID
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    comment: str | None = None
    discount_percent: float = 0


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    organization_id: UUID | None = None
    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    comment: str | None = None
    discount_percent: float | None = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
