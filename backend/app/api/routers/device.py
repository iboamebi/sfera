"""
Device actions.
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

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post("/{device_id}/connect")
def connect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(get_device_service),
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


@router.post("/{device_id}/disconnect")
def disconnect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(get_device_service),
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
