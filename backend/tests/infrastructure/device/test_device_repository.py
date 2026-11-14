from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)


def test_device_repository_class_exists():
    assert DeviceRepositorySQLAlchemy is not None



def test_device_repository_checks_serial_with_customer_and_type():
    from unittest.mock import MagicMock
    from uuid import uuid4

    from app.infrastructure.device.device_repository import (
        DeviceRepositorySQLAlchemy,
    )

    session = MagicMock()
    query = session.query.return_value
    query.filter.return_value = query
    query.first.return_value = None
    repository = DeviceRepositorySQLAlchemy(session)

    assert not repository.exists_by_customer_type_and_serial_number(
        uuid4(),
        uuid4(),
        "SN-001",
    )
    assert query.filter.call_count == 1
