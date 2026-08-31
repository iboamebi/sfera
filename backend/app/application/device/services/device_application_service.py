"""Application service for Device."""

from uuid import UUID, uuid4

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
from app.domains.device.entities.device import Device
from app.domains.device.exceptions import (
    DeviceNotAvailableDomainError,
    DeviceNotInWorkDomainError,
)
from app.domains.device.factories.device_factory import DeviceFactory
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class DeviceApplicationService:
    """Coordinates Device use cases."""

    def __init__(
        self,
        repository: DeviceRepository,
        instrument_type_repository: InstrumentTypeRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._instrument_type_repository = instrument_type_repository
        self._uow = unit_of_work

    def create(
        self,
        command: CreateDeviceCommand,
    ) -> Device:
        """Create device."""

        with self._uow:
            instrument_type = self._instrument_type_repository.get(
                command.instrument_type_id,
            )

            if instrument_type is None:
                raise InstrumentTypeNotFoundApplicationError

            device = DeviceFactory.create(
                device_id=uuid4(),
                instrument_type_id=command.instrument_type_id,
                serial_number=command.serial_number,
            )

            self._repository.save(device)

        return device

    def list(self) -> list[Device]:
        """List devices."""

        return self._repository.list()

    def get(
        self,
        device_id: UUID,
    ) -> Device:
        """Get device."""

        device = self._repository.get(device_id)

        if device is None:
            raise DeviceNotFoundApplicationError

        return device

    def update(
        self,
        command: UpdateDeviceCommand,
    ) -> Device:
        """Update an instrument card."""

        with self._uow:
            device = self.get(command.device_id)
            device.serial_number = type(device.serial_number)(command.serial_number)
            device.registry_number = command.registry_number
            device.modification = command.modification
            device.factory_number = command.factory_number
            device.manufacture_year = command.manufacture_year
            device.inventory_number = command.inventory_number
            device.comment = command.comment
            self._repository.save(device)

        return device

    def connect(
        self,
        command: ConnectDeviceCommand,
    ) -> Device:
        """Connect device."""

        with self._uow:
            device = self.get(command.device_id)

            try:
                device.connect()

            except DeviceNotAvailableDomainError:
                raise DeviceNotAvailableApplicationError from None

            self._repository.save(device)

        return device

    def disconnect(
        self,
        command: DisconnectDeviceCommand,
    ) -> Device:
        """Disconnect device."""

        with self._uow:
            device = self.get(command.device_id)

            try:
                device.disconnect()

            except DeviceNotInWorkDomainError:
                raise DeviceNotInWorkApplicationError from None

            self._repository.save(device)

        return device
