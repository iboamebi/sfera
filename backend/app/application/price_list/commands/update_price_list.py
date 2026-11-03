# Update PriceList command.
# Defines input data for updating an existing PriceList aggregate.

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class UpdatePriceListCommand:
    """
    Command for updating an existing PriceList.
    """

    price_list_id: UUID
    name: str | None = None
    price_list_type: str | None = None
    currency: str | None = None
    description: str | None = None
    is_active: bool | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    updated_fields: frozenset[str] = frozenset()
