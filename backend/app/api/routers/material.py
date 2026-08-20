"""
Material API router.

Handles HTTP endpoints for material operations.
Version: 2.0
Revision: 2026-08-11
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.material.commands.archive_material import (
    ArchiveMaterialCommand,
)
from app.application.material.commands.create_material import (
    CreateMaterialCommand,
)
from app.application.material.commands.restore_material import (
    RestoreMaterialCommand,
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
from app.domains.user.entities.user import User
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
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def create_material(
    data: MaterialCreate,
    user: User = Depends(get_current_user),
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

    return service.create(command, user)


@router.put(
    "/{material_id}",
    response_model=MaterialRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def update_material(
    material_id: UUID,
    data: MaterialUpdate,
    user: User = Depends(get_current_user),
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

    return service.update(command, user)


@router.post(
    "/{material_id}/archive",
    response_model=MaterialRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def archive_material(
    material_id: UUID,
    user: User = Depends(get_current_user),
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    command = ArchiveMaterialCommand(
        material_id=material_id,
    )

    return service.archive(command, user)


@router.post(
    "/{material_id}/restore",
    response_model=MaterialRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def restore_material(
    material_id: UUID,
    user: User = Depends(get_current_user),
    service: MaterialApplicationService = Depends(
        get_material_service,
    ),
):
    command = RestoreMaterialCommand(
        material_id=material_id,
    )

    return service.restore(command, user)
