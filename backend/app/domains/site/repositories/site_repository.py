"""Site repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.site.entities.site import Site


class SiteRepository(ABC):
    """Abstract site repository."""

    @abstractmethod
    def get(
        self,
        site_id: UUID,
    ) -> Site | None:
        """Get site by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Site]:
        """Get all sites."""

        raise NotImplementedError

    @abstractmethod
    def get_by_organization_id(
        self,
        organization_id: UUID,
    ) -> list[Site]:
        """Get sites belonging to an organization."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        site: Site,
    ) -> Site:
        """Save site."""

        raise NotImplementedError
