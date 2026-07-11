from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MaterialBase(BaseModel):
    name: str
    article: str | None = None
    unit: str
    description: str | None = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: str | None = None
    article: str | None = None
    unit: str | None = None
    description: str | None = None


class MaterialRead(MaterialBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
