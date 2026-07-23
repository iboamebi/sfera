from enum import StrEnum


class DeviceStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
