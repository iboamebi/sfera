"""
Application service for Customer ↔ Organization associations.
"""

from uuid import UUID

from app.application.authorization.authorization import require_role
from app.application.customer.commands.add_customer_organization import (
    AddCustomerOrganizationCommand,
)
from app.application.customer.commands.unlink_customer_organization import (
    UnlinkCustomerOrganizationCommand,
)
from app.application.customer.customer_organization_exceptions import (
    CustomerOrganizationAlreadyLinkedApplicationError,
    CustomerOrganizationLinkNotFoundApplicationError,
    CustomerOrganizationNotFoundApplicationError,
)
from app.domains.customer.repositories.customer_organization_repository import (
    CustomerOrganizationRepository,
)
from app.domains.customer.repositories.customer_repository import CustomerRepository
from app.domains.organization.entities.organization import Organization
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class CustomerOrganizationApplicationService:
    """Coordinates Customer ↔ Organization association use cases."""

    def __init__(
        self,
        customer_repository: CustomerRepository,
        organization_repository: OrganizationRepository,
        association_repository: CustomerOrganizationRepository,
        uow: UnitOfWork,
    ) -> None:
        self._customer_repository = customer_repository
        self._organization_repository = organization_repository
        self._association_repository = association_repository
        self._uow = uow

    def get_organizations(self, customer_id: UUID) -> list[Organization]:
        if self._customer_repository.get(customer_id) is None:
            raise CustomerOrganizationNotFoundApplicationError

        return self._association_repository.get_organizations(customer_id)

    def add(
        self,
        command: AddCustomerOrganizationCommand,
        user: User,
    ) -> Organization:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        if self._customer_repository.get(command.customer_id) is None:
            raise CustomerOrganizationNotFoundApplicationError

        organization = self._organization_repository.get(
            command.organization_id,
        )
        if organization is None:
            raise CustomerOrganizationNotFoundApplicationError

        existing = self._association_repository.get_organizations(
            command.customer_id,
        )
        if any(item.id == organization.id for item in existing):
            raise CustomerOrganizationAlreadyLinkedApplicationError

        with self._uow:
            self._association_repository.add(
                command.customer_id,
                command.organization_id,
            )

        return organization

    def unlink(
        self,
        command: UnlinkCustomerOrganizationCommand,
        user: User,
    ) -> None:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        if self._customer_repository.get(command.customer_id) is None:
            raise CustomerOrganizationNotFoundApplicationError

        existing = self._association_repository.get_organizations(
            command.customer_id,
        )
        if not any(item.id == command.organization_id for item in existing):
            raise CustomerOrganizationLinkNotFoundApplicationError

        with self._uow:
            self._association_repository.remove(
                command.customer_id,
                command.organization_id,
            )
