"""Application use case for controlled instrument Site reassignment."""

from app.application.device.commands.change_device_site import (
    ChangeDeviceSiteCommand,
)
from app.application.device.exceptions import (
    DeviceNotFoundApplicationError,
    DeviceSiteChangeReasonRequiredApplicationError,
    SiteCustomerMismatchApplicationError,
    SiteNotFoundApplicationError,
)
from app.domains.device.entities.device import Device
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.site.repositories.site_repository import SiteRepository
from app.domains.user.entities.user import User
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class DeviceSiteAssignmentApplicationService:
    """Coordinates documented changes to an instrument's Site assignment."""

    def __init__(
        self,
        device_repository: DeviceRepository,
        site_repository: SiteRepository,
        unit_of_work: UnitOfWork,
        audit_operation_repository: AuditOperationRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self._device_repository = device_repository
        self._site_repository = site_repository
        self._uow = unit_of_work
        self._audit_operation_repository = audit_operation_repository
        self._audit_repository = audit_repository

    def change_site(
        self,
        command: ChangeDeviceSiteCommand,
        user: User,
    ) -> Device:
        """Change or clear Site assignment and persist its audit history."""
        reason = command.reason.strip()
        if not reason:
            raise DeviceSiteChangeReasonRequiredApplicationError

        with self._uow:
            device = self._device_repository.get(command.device_id)
            if device is None:
                raise DeviceNotFoundApplicationError

            new_site = None
            if command.site_id is not None:
                new_site = self._site_repository.get(command.site_id)
                if new_site is None:
                    raise SiteNotFoundApplicationError
                if new_site.customer_id != device.customer_id:
                    raise SiteCustomerMismatchApplicationError

            old_site_id = device.site_id
            if old_site_id == command.site_id:
                return device

            old_site = (
                self._site_repository.get(old_site_id)
                if old_site_id is not None
                else None
            )

            device.change_site(command.site_id)
            self._device_repository.save(device)

            operation = AuditOperation(initiated_by=user.id)
            self._audit_operation_repository.save(operation)
            self._audit_repository.save(
                AuditRecord(
                    operation_id=operation.operation_id,
                    actor_id=user.id,
                    action="instrument.site_changed",
                    entity_type="Instrument",
                    entity_id=device.id,
                    changes={
                        "site": {
                            "old": {
                                "id": str(old_site_id) if old_site_id else None,
                                "name": old_site.name if old_site else None,
                            },
                            "new": {
                                "id": str(new_site.id) if new_site else None,
                                "name": new_site.name if new_site else None,
                            },
                        },
                    },
                    reason=reason,
                )
            )

        return device
