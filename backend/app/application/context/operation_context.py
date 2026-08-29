"""Application operation context."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class OperationContext:
    """Carry operation-level execution metadata across application use cases."""

    operation_id: UUID
    actor_id: UUID | None = None
