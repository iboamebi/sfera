from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=False)
class Entity:
    id: UUID

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
        )

    def __hash__(self) -> int:
        return hash(self.id)
