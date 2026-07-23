from enum import StrEnum


class OrderStatus(StrEnum):
    NEW = "NEW"
    REGISTERED = "REGISTERED"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    ISSUED = "ISSUED"
    CLOSED = "CLOSED"


class OrderItemStatus(StrEnum):
    RECEIVED = "RECEIVED"  # принят в работу
    IN_DIAGNOSTIC = "IN_DIAGNOSTIC"
    IN_VERIFICATION = "IN_VERIFICATION"
    IN_REPAIR = "IN_REPAIR"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    ISSUED = "ISSUED"


class VerificationResult(StrEnum):
    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"
