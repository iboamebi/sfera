from dataclasses import dataclass
from datetime import datetime, UTC
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: datetime

    @classmethod
    def create(cls):
        return cls(
            event_id=str(uuid4()),
            occurred_at=datetime.now(UTC),
        )
