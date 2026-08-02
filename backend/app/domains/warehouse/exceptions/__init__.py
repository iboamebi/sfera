"""
Warehouse domain exceptions.
"""

from app.domains.warehouse.exceptions.warehouse_exception import (
    WarehouseException,
)


class InvalidWarehouseQuantityDomainError(WarehouseException):
    """Warehouse quantity must be positive."""


class InsufficientWarehouseStockDomainError(WarehouseException):
    """Warehouse stock quantity is insufficient."""


class InsufficientReservedQuantityDomainError(WarehouseException):
    """Reserved quantity is insufficient."""
