from app.crud.base import BaseCRUD
from app.models.repair import Repair
from app.schemas.repair import (
    RepairCreate,
    RepairUpdate,
)


class RepairCRUD(
    BaseCRUD[
        Repair,
        RepairCreate,
        RepairUpdate,
    ]
):
    pass


repair_crud = RepairCRUD(Repair)
