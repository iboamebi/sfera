class StockNotFoundApplicationError(Exception):
    """Stock not found."""


class UnsupportedWarehouseMovementApplicationError(Exception):
    """Movement type is not supported by stock operations."""
