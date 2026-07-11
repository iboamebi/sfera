from dataclasses import dataclass
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False)
class OrderItem(Entity):
    instrument_id: UUID | None = None
    comment: str | None = None
