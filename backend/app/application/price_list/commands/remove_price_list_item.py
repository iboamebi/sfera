# Remove PriceListItem command.
# Defines input data for removing an item from a PriceList aggregate.

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RemovePriceListItemCommand:
    """
    Command for removing an item from PriceList.
    """

    price_list_id: UUID
    item_id: UUID
