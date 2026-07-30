"""
Material API router.
"""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.application.material.commands.create_material import (
    CreateMaterialCommand,
)
from app.application.material.commands.update_material import (
    UpdateMaterialCommand,
)
from app.application.material.services.material_application_service import (
    MaterialApplicationService,
)
from app.core.dependencies.services import get_material_service
from app.schemas.material import (
    MaterialCreate,
    MaterialRead,
    MaterialUpdate,
)

router = APIRouter(
    prefix="/materials",
    tags=["Materials"],
)


@router.get(
    "/",
    response_model=list[MaterialRead],
)
def get_materials(
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    return service.get_all()


@router.get(
    "/{material_id}",
    response_model=MaterialRead,
)
def get_material(
    material_id: UUID,
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    try:
        return service.get(material_id)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Material not found",
        ) from None


@router.post(
    "/",
    response_model=MaterialRead,
    status_code=201,
)
def create_material(
    data: MaterialCreate,
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    command = CreateMaterialCommand(
        material_id=uuid4(),
        name=data.name,
        article=data.article,
        unit=data.unit,
        description=data.description,
    )

    return service.create(command)


@router.put(
    "/{material_id}",
    response_model=MaterialRead,
)
def update_material(
    material_id: UUID,
    data: MaterialUpdate,
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    command = UpdateMaterialCommand(
        material_id=material_id,
        **data.model_dump(
            exclude_unset=True,
        ),
    )

    return service.update(command)


@router.delete(
    "/{material_id}",
    status_code=204,
)
def delete_material(
    material_id: UUID,
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    service.delete(material_id)
