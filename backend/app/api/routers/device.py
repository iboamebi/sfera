"""
Device actions.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

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
    device = service.connect(device_id)

    return {
        "event": "DeviceConnected",
        "device_id": device.id,
    }


@router.post("/{device_id}/disconnect")
def disconnect_device(
    device_id: UUID,
    service: DeviceApplicationService = Depends(get_device_service),
):
    device = service.disconnect(device_id)

    return {
        "event": "DeviceDisconnected",
        "device_id": device.id,
    }
