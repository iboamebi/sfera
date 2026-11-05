"""
Application service: Site.
"""

from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.site.commands.create_site import CreateSiteCommand
from app.domains.site.entities.site import Site
from app.domains.site.repositories.site_repository import SiteRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class SiteApplicationService:
    """Site application service."""

    def __init__(
        self,
        repository: SiteRepository,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    def get(
        self,
        site_id: UUID,
    ) -> Site | None:
        """Get site by identifier."""

        return self._repository.get(site_id)

    def get_all(self) -> list[Site]:
        """Get all sites."""

        return self._repository.get_all()

    def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> list[Site]:
        """Get sites belonging to a customer."""

        return self._repository.get_by_customer_id(customer_id)

    def create(
        self,
        command: CreateSiteCommand,
        user: User,
    ) -> Site:
        """Create site."""

        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            site = Site(
                id=uuid4(),
                customer_id=command.customer_id,
                name=command.name,
                address=command.address,
            )

            return self._repository.save(site)
