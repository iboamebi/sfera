"""
Device actions.

Handles HTTP endpoints for device business actions.
Version: 2.0
Revision: 2026-08-11
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.device.exceptions import (
    DeviceNotAvailableApplicationError,
    DeviceNotFoundApplicationError,
    DeviceNotInWorkApplicationError,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.core.dependencies.services import get_device_service
from app.schemas.device_action import DeviceActionResponse

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post(
    "/{device_id}/connect",
    response_model=DeviceActionResponse,
)
def connect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        device = service.connect(device_id)

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
)
def disconnect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(
        get_device_service,
    ),
):
    try:
        device = service.disconnect(device_id)

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
