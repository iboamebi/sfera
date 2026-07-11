from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.diagnostic import Recommendation


class DiagnosticBase(BaseModel):
    order_item_id: UUID
    conclusion: str | None = None
    recommendation: Recommendation | None = None


class DiagnosticCreate(DiagnosticBase):
    pass


class DiagnosticUpdate(BaseModel):
    conclusion: str | None = None
    recommendation: Recommendation | None = None


class DiagnosticRead(DiagnosticBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
