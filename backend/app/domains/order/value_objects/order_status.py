from enum import StrEnum


class OrderStatus(StrEnum):
    NEW = "NEW"
    REGISTERED = "REGISTERED"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    ISSUED = "ISSUED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
