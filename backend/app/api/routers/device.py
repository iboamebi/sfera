from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.device.commands.connect_device import (
    ConnectDeviceCommand,
    ConnectDeviceHandler,
)
from app.application.device.commands.disconnect_device import (
    DisconnectDeviceCommand,
    DisconnectDeviceHandler,
)
from app.db.database import get_db
from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post("/{device_id}/connect")
def connect_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DeviceRepositorySQLAlchemy(db)

    device = repository.get(device_id)

    if device is None:
        return {"error": "Device not found"}

    event = ConnectDeviceHandler().handle(ConnectDeviceCommand(device))

    repository.save(device)

    return {
        "event": "DeviceConnected",
        "device_id": event.device_id,
    }


@router.post("/{device_id}/disconnect")
def disconnect_device(
    device_id: UUID,
    db: Session = Depends(get_db),
):
    repository = DeviceRepositorySQLAlchemy(db)

    device = repository.get(device_id)

    if device is None:
        return {"error": "Device not found"}

    event = DisconnectDeviceHandler().handle(DisconnectDeviceCommand(device))

    repository.save(device)

    return {
        "event": "DeviceDisconnected",
        "device_id": event.device_id,
    }
