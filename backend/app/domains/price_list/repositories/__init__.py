# PriceList domain repositories package.
# Exports repository interfaces for the PriceList context.

from app.domains.price_list.repositories.price_list_repository import (
    PriceListRepository,
)

__all__ = [
    "PriceListRepository",
]
