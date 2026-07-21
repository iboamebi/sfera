from enum import Enum


class OrderStatus(str, Enum):
    NEW = "NEW"
    REGISTERED = "REGISTERED"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    ISSUED = "ISSUED"
    CLOSED = "CLOSED"


class OrderItemStatus(str, Enum):
    RECEIVED = "RECEIVED"  # принят в работу
    IN_DIAGNOSTIC = "IN_DIAGNOSTIC"
    IN_VERIFICATION = "IN_VERIFICATION"
    IN_REPAIR = "IN_REPAIR"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    ISSUED = "ISSUED"


class VerificationResult(str, Enum):
    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"
