"""
InstrumentType API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.instrument_type.commands.archive_instrument_type import (
    ArchiveInstrumentTypeCommand,
)
from app.application.instrument_type.commands.create_instrument_type import (
    CreateInstrumentTypeCommand,
)
from app.application.instrument_type.commands.restore_instrument_type import (
    RestoreInstrumentTypeCommand,
)
from app.application.instrument_type.commands.update_instrument_type import (
    UpdateInstrumentTypeCommand,
)
from app.application.instrument_type.exceptions import (
    InstrumentTypeNotFoundApplicationError,
)
from app.application.instrument_type.services import (
    instrument_type_application_service as instrument_type_service,
)
from app.core.dependencies.services import get_instrument_type_service
from app.schemas.instrument_type import (
    InstrumentTypeCreate,
    InstrumentTypeRead,
    InstrumentTypeUpdate,
)

router = APIRouter(
    prefix="/instrument-types",
    tags=["InstrumentTypes"],
)


@router.post(
    "/",
    response_model=InstrumentTypeRead,
    status_code=201,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def create_instrument_type(
    data: InstrumentTypeCreate,
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    command = CreateInstrumentTypeCommand(
        **data.model_dump(),
    )

    return service.create(command)


@router.get(
    "/",
    response_model=list[InstrumentTypeRead],
)
def get_instrument_types(
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    return service.get_all()


@router.get(
    "/{instrument_type_id}",
    response_model=InstrumentTypeRead,
)
def get_instrument_type(
    instrument_type_id: UUID,
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    try:
        return service.get(instrument_type_id)

    except InstrumentTypeNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Instrument type not found",
        ) from None


@router.put(
    "/{instrument_type_id}",
    response_model=InstrumentTypeRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def update_instrument_type(
    instrument_type_id: UUID,
    data: InstrumentTypeUpdate,
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    command = UpdateInstrumentTypeCommand(
        instrument_type_id=instrument_type_id,
        **data.model_dump(
            exclude_unset=True,
        ),
    )

    return service.update(command)


@router.post(
    "/{instrument_type_id}/archive",
    response_model=InstrumentTypeRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def archive_instrument_type(
    instrument_type_id: UUID,
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    command = ArchiveInstrumentTypeCommand(
        instrument_type_id=instrument_type_id,
    )

    try:
        return service.archive(command)

    except InstrumentTypeNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Instrument type not found",
        ) from None


@router.post(
    "/{instrument_type_id}/restore",
    response_model=InstrumentTypeRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def restore_instrument_type(
    instrument_type_id: UUID,
    service: instrument_type_service.InstrumentTypeApplicationService = Depends(
        get_instrument_type_service,
    ),
):
    command = RestoreInstrumentTypeCommand(
        instrument_type_id=instrument_type_id,
    )

    try:
        return service.restore(command)

    except InstrumentTypeNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Instrument type not found",
        ) from None
