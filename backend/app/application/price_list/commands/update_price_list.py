# Update PriceList command.
# Defines input data for updating an existing PriceList aggregate.

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdatePriceListCommand:
    """
    Command for updating an existing PriceList.
    """

    price_list_id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
