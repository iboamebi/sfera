# Activate PriceList command.
# Defines input data for activating a PriceList aggregate.

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ActivatePriceListCommand:
    """
    Command for activating a PriceList.
    """

    price_list_id: UUID
