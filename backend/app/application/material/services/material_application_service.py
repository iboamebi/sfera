"""
Application service for Material.
"""

from uuid import UUID

from app.application.material.commands.create_material import (
    CreateMaterialCommand,
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
    ) -> Material:
        """Create material."""

        material = Material(
            id=command.material_id,
            name=command.name,
            article=command.article,
            unit=command.unit,
            description=command.description,
        )

        return self._repository.save(material)

    def update(
        self,
        command: UpdateMaterialCommand,
    ) -> Material:
        """Update material."""

        material = self.get(command.material_id)

        if command.name is not None:
            material.name = command.name

        if command.article is not None:
            material.article = command.article

        if command.unit is not None:
            material.unit = command.unit

        if command.description is not None:
            material.description = command.description

        return self._repository.save(material)

    def delete(
        self,
        material_id: UUID,
    ) -> None:
        """Delete material."""

        self._repository.delete(material_id)
