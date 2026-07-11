from app.api.base_router import BaseRouter
from app.crud.price_list_item import price_list_item_crud
from app.schemas.price_list_item import (
    PriceListItemCreate,
    PriceListItemRead,
    PriceListItemUpdate,
)

router = BaseRouter(
    crud=price_list_item_crud,
    read_schema=PriceListItemRead,
    create_schema=PriceListItemCreate,
    update_schema=PriceListItemUpdate,
    prefix="/price-list-items",
    tags=["Price List Items"],
).router
