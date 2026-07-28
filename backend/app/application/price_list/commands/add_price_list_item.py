# Add PriceListItem command.
# Defines input data for adding a new item to a PriceList aggregate.

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class AddPriceListItemCommand:
    """
    Command for adding an item to PriceList.
    """

    price_list_id: UUID
    service_code: str
    name: str
    price: Decimal
    unit: str = "pcs"
    description: str | None = None
