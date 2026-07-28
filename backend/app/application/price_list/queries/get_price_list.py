# Get PriceList query.
# Defines input data for retrieving a PriceList by identifier.

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetPriceListQuery:
    """
    Query for retrieving PriceList by id.
    """

    price_list_id: UUID
