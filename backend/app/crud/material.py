from app.crud.base import BaseCRUD
from app.models.material import Material
from app.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
)


class MaterialCRUD(
    BaseCRUD[
        Material,
        MaterialCreate,
        MaterialUpdate,
    ]
):
    pass


material_crud = MaterialCRUD(Material)
