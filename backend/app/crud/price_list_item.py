from app.crud.base import BaseCRUD
from app.models.price_list_item import PriceListItem
from app.schemas.price_list_item import (
    PriceListItemCreate,
    PriceListItemUpdate,
)


class PriceListItemCRUD(
    BaseCRUD[
        PriceListItem,
        PriceListItemCreate,
        PriceListItemUpdate,
    ]
):
    pass


price_list_item_crud = PriceListItemCRUD(PriceListItem)
