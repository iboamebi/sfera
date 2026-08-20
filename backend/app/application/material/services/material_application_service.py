"""
Application service for Material.
"""

from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.material.commands.archive_material import (
    ArchiveMaterialCommand,
)
from app.application.material.commands.create_material import (
    CreateMaterialCommand,
)
from app.application.material.commands.restore_material import (
    RestoreMaterialCommand,
)
from app.application.material.commands.update_material import (
    UpdateMaterialCommand,
)
from app.application.material.exceptions import (
    MaterialNotFoundApplicationError,
)
from app.domains.material.entities.material import Material
from app.domains.material.repositories.material_repository import (
    MaterialRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole


class MaterialApplicationService:
    """Coordinates Material use cases."""

    def __init__(
        self,
        repository: MaterialRepository,
    ) -> None:
        self._repository = repository

    def get(
        self,
        material_id: UUID,
    ) -> Material:
        """Get material."""

        material = self._repository.get(material_id)

        if material is None:
            raise MaterialNotFoundApplicationError

        return material

    def get_all(
        self,
    ) -> list[Material]:
        """Get all materials."""

        return self._repository.get_all()

    def create(
        self,
        command: CreateMaterialCommand,
        user: User,
    ) -> Material:
        """Create material."""

        require_role(
            user,
            UserRole.OPERATOR,
            UserRole.ADMIN,
            UserRole.WAREHOUSE,
        )

        material = Material(
            id=uuid4(),
            name=command.name,
            article=command.article,
            unit=command.unit,
            description=command.description,
        )

        return self._repository.save(material)

    def update(
        self,
        command: UpdateMaterialCommand,
        user: User,
    ) -> Material:
        """Update material."""

        require_role(
            user,
            UserRole.OPERATOR,
            UserRole.ADMIN,
            UserRole.WAREHOUSE,
        )

        material = self.get(
            command.material_id,
        )

        if command.name is not None:
            material.change_name(
                command.name,
            )

        if command.article is not None:
            material.change_article(
                command.article,
            )

        if command.unit is not None:
            material.change_unit(
                command.unit,
            )

        if command.description is not None:
            material.change_description(
                command.description,
            )

        return self._repository.save(material)

    def archive(
        self,
        command: ArchiveMaterialCommand,
        user: User,
    ) -> Material:
        """Archive material."""

        require_role(
            user,
            UserRole.OPERATOR,
            UserRole.ADMIN,
            UserRole.WAREHOUSE,
        )

        material = self.get(
            command.material_id,
        )

        material.archive()

        return self._repository.save(material)

    def restore(
        self,
        command: RestoreMaterialCommand,
        user: User,
    ) -> Material:
        """Restore material."""

        require_role(
            user,
            UserRole.OPERATOR,
            UserRole.ADMIN,
            UserRole.WAREHOUSE,
        )

        material = self.get(
            command.material_id,
        )

        material.restore()

        return self._repository.save(material)
