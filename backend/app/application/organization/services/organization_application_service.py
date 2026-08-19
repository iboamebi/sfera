"""
Application service: Organization.
"""

from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.organization.commands.create_organization import (
    CreateOrganizationCommand,
)
from app.application.organization.commands.update_organization import (
    UpdateOrganizationCommand,
)
from app.application.organization.exceptions import (
    OrganizationNotFoundApplicationError,
)
from app.domains.organization.entities.organization import Organization
from app.domains.organization.exceptions import OrganizationNotFoundError
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class OrganizationApplicationService:
    """Organization application service."""

    def __init__(
        self,
        repository: OrganizationRepository,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    def create(
        self,
        command: CreateOrganizationCommand,
        user: User,
    ) -> Organization:
        """Create organization."""

        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            organization = Organization(
                id=uuid4(),
                name=command.name,
                short_name=command.short_name,
                inn=command.inn,
                kpp=command.kpp,
                ogrn=command.ogrn,
                address=command.address,
                phone=command.phone,
                email=command.email,
                website=command.website,
                comment=command.comment,
            )

            return self._repository.save(organization)

    def get(
        self,
        organization_id: UUID,
    ) -> Organization:
        """Get organization by identifier."""

        organization = self._repository.get(
            organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundApplicationError from OrganizationNotFoundError

        return organization

    def get_all(
        self,
    ) -> list[Organization]:
        """Get all organizations."""

        return self._repository.get_all()

    def update(
        self,
        command: UpdateOrganizationCommand,
        user: User,
    ) -> Organization:
        """Update organization."""

        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            organization = self.get(
                command.organization_id,
            )

            if command.name is not None:
                organization.change_name(
                    command.name,
                )

            if command.short_name is not None:
                organization.change_short_name(
                    command.short_name,
                )

            if command.inn is not None:
                organization.change_inn(
                    command.inn,
                )

            if command.kpp is not None:
                organization.change_kpp(
                    command.kpp,
                )

            if command.ogrn is not None:
                organization.change_ogrn(
                    command.ogrn,
                )

            if command.address is not None:
                organization.change_address(
                    command.address,
                )

            if command.phone is not None:
                organization.change_phone(
                    command.phone,
                )

            if command.email is not None:
                organization.change_email(
                    command.email,
                )

            if command.website is not None:
                organization.change_website(
                    command.website,
                )

            if command.comment is not None:
                organization.change_comment(
                    command.comment,
                )

            return self._repository.save(organization)
