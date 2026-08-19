from uuid import uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.material.commands.create_material import CreateMaterialCommand
from app.application.material.commands.update_material import UpdateMaterialCommand
from app.application.material.services.material_application_service import (
    MaterialApplicationService,
)
from app.domains.material.entities.material import Material
from app.domains.material.repositories.material_repository import MaterialRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole


class FakeMaterialRepository(MaterialRepository):
    def __init__(self) -> None:
        self._materials: dict[object, Material] = {}

    def get(self, material_id, include_archived: bool = False):
        material = self._materials.get(material_id)
        if material is None or (material.archived and not include_archived):
            return None
        return material

    def get_all(self, include_archived: bool = False):
        return [
            material
            for material in self._materials.values()
            if include_archived or not material.archived
        ]

    def save(self, material: Material) -> Material:
        self._materials[material.id] = material
        return material


def make_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        username=f"test-{role.value}",
        password_hash="hash",
        role=role,
    )


def test_update_material_allows_warehouse_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = service.create(
        CreateMaterialCommand(
            name="Original Material",
            article="A-001",
            unit="pcs",
            description="Original description",
        )
    )

    updated = service.update(
        UpdateMaterialCommand(
            material_id=material.id,
            name="Updated Material",
            article="A-002",
            unit="kg",
            description="Updated description",
        ),
        make_user(UserRole.WAREHOUSE),
    )

    assert updated is material
    assert updated.name == "Updated Material"
    assert updated.article == "A-002"
    assert updated.unit == "kg"
    assert updated.description == "Updated description"


def test_update_material_rejects_unauthorized_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = service.create(
        CreateMaterialCommand(
            name="Protected Material",
            article="A-001",
            unit="pcs",
            description="Protected description",
        )
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.update(
            UpdateMaterialCommand(
                material_id=material.id,
                name="Unauthorized Update",
            ),
            make_user(UserRole.TECHNICIAN),
        )

    assert material.name == "Protected Material"
