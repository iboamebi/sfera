from dataclasses import dataclass
from uuid import UUID

from app.shared.events.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class OrderRegistered(DomainEvent):
    order_id: UUID
