from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.routers.device import change_device_site
from app.application.device.commands.change_device_site import (
    ChangeDeviceSiteCommand,
)
from app.application.device.exceptions import (
    DeviceNotFoundApplicationError,
    SiteCustomerMismatchApplicationError,
    SiteNotFoundApplicationError,
)
from app.domains.device.entities.device import Device
from app.domains.device.value_objects.serial_number import SerialNumber
from app.schemas.device import DeviceSiteChange


def make_device() -> Device:
    return Device(
        id=uuid4(),
        instrument_type_id=uuid4(),
        customer_id=uuid4(),
        serial_number=SerialNumber("SN-001"),
    )


def test_change_device_site_forwards_command_and_user() -> None:
    device = make_device()
    user = object()

    class FakeService:
        def change_site(self, command: ChangeDeviceSiteCommand, actor: object):
            assert command == ChangeDeviceSiteCommand(
                device_id=device.id,
                site_id=None,
                reason="Approved removal",
            )
            assert actor is user
            return device

    result = change_device_site(
        device_id=device.id,
        data=DeviceSiteChange(
            site_id=None,
            reason=" Approved removal ",
        ),
        user=user,
        service=FakeService(),
    )

    assert result is device


@pytest.mark.parametrize(
    ("error", "status_code", "detail"),
    [
        (DeviceNotFoundApplicationError, 404, "Device not found"),
        (SiteNotFoundApplicationError, 404, "Site not found"),
        (
            SiteCustomerMismatchApplicationError,
            409,
            "Site does not belong to device customer",
        ),
    ],
)
def test_change_device_site_maps_application_errors(
    error: type[Exception],
    status_code: int,
    detail: str,
) -> None:
    device_id = uuid4()

    class FakeService:
        def change_site(self, command: ChangeDeviceSiteCommand, actor: object):
            raise error

    with pytest.raises(HTTPException) as exc_info:
        change_device_site(
            device_id=device_id,
            data=DeviceSiteChange(
                site_id=uuid4(),
                reason="Documented change",
            ),
            user=object(),
            service=FakeService(),
        )

    assert exc_info.value.status_code == status_code
    assert exc_info.value.detail == detail


def test_device_site_change_schema_requires_nonblank_reason() -> None:
    with pytest.raises(ValueError):
        DeviceSiteChange(site_id=None, reason="   ")
