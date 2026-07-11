from app.api.base_router import BaseRouter
from app.crud.repair import repair_crud
from app.schemas.repair import (
    RepairCreate,
    RepairRead,
    RepairUpdate,
)

router = BaseRouter(
    crud=repair_crud,
    read_schema=RepairRead,
    create_schema=RepairCreate,
    update_schema=RepairUpdate,
    prefix="/repairs",
    tags=["Repairs"],
).router
