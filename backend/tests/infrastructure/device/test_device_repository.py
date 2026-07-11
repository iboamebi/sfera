from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)


def test_device_repository_class_exists():

    assert DeviceRepositorySQLAlchemy is not None
