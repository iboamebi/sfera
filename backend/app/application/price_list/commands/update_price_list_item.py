# Update PriceListItem command.
# Defines input data for updating an existing item in a PriceList aggregate.

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class UpdatePriceListItemCommand:
    """
    Command for updating an item in PriceList.
    """

    price_list_id: UUID
    item_id: UUID
    price: Decimal | None = None
    description: str | None = None
