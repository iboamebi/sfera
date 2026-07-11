from dataclasses import dataclass

from app.shared.events.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class DeviceConnected(DomainEvent):
    device_id: str
