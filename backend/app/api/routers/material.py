"""
Material API router.

Handles HTTP endpoints for material operations.
Version: 2.0
Revision: 2026-08-11
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.material.commands.archive_material import (
    ArchiveMaterialCommand,
)
from app.application.material.commands.create_material import (
    CreateMaterialCommand,
)
from app.application.material.commands.update_material import (
    UpdateMaterialCommand,
)
from app.application.material.exceptions import (
    MaterialNotFoundApplicationError,
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

    except MaterialNotFoundApplicationError:
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


@router.post(
    "/{material_id}/archive",
    response_model=MaterialRead,
)
def archive_material(
    material_id: UUID,
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    command = ArchiveMaterialCommand(
        material_id=material_id,
    )

    return service.archive(command)
