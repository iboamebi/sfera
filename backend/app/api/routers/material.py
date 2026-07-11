from app.api.base_router import BaseRouter
from app.crud.material import material_crud
from app.schemas.material import (
    MaterialCreate,
    MaterialRead,
    MaterialUpdate,
)

router = BaseRouter(
    crud=material_crud,
    read_schema=MaterialRead,
    create_schema=MaterialCreate,
    update_schema=MaterialUpdate,
    prefix="/materials",
    tags=["Materials"],
).router
