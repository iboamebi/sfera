"""
Device API router.

Handles HTTP endpoints for device operations.
Version: 3.0
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.device.commands.connect_device import ConnectDeviceCommand
from app.application.device.commands.create_device import CreateDeviceCommand
from app.application.device.commands.disconnect_device import DisconnectDeviceCommand
from app.application.device.commands.update_device import UpdateDeviceCommand
from app.application.device.exceptions import (
    DeviceNotAvailableApplicationError,
    DeviceNotFoundApplicationError,
    DeviceNotInWorkApplicationError,
    InstrumentTypeNotFoundApplicationError,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.core.dependencies.services import get_device_service
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.schemas.device_action import DeviceActionResponse

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.get(
    "/",
    response_model=list[DeviceRead],
)
def list_devices(
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    return service.list()


@router.get(
    "/{device_id}",
    response_model=DeviceRead,
)
def get_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        return service.get(device_id)
    except DeviceNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Device not found") from None


@router.post(
    "/",
    response_model=DeviceRead,
    status_code=201,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def create_device(
    data: DeviceCreate,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    command = CreateDeviceCommand(
        **data.model_dump(),
    )

    try:
        return service.create(command)

    except InstrumentTypeNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Instrument type not found",
        ) from None


@router.put(
    "/{device_id}",
    response_model=DeviceRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def update_device(
    device_id: UUID,
    data: DeviceUpdate,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        return service.update(
            UpdateDeviceCommand(
                device_id=device_id,
                **data.model_dump(exclude_unset=True),
            ),
        )

    except DeviceNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        ) from None

    except InstrumentTypeNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Instrument type not found",
        ) from None


@router.post(
    "/{device_id}/connect",
    response_model=DeviceActionResponse,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def connect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        device = service.connect(
            ConnectDeviceCommand(
                device_id=device_id,
            ),
        )

    except DeviceNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        ) from None

    except DeviceNotAvailableApplicationError:
        raise HTTPException(
            status_code=409,
            detail="Device is not available",
        ) from None

    return {
        "event": "DeviceConnected",
        "device_id": device.id,
    }


@router.post(
    "/{device_id}/disconnect",
    response_model=DeviceActionResponse,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def disconnect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        device = service.disconnect(
            DisconnectDeviceCommand(
                device_id=device_id,
            ),
        )

    except DeviceNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        ) from None

    except DeviceNotInWorkApplicationError:
        raise HTTPException(
            status_code=409,
            detail="Device is not in work",
        ) from None

    return {
        "event": "DeviceDisconnected",
        "device_id": device.id,
    }
