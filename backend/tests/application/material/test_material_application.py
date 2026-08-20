from uuid import uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.material.commands.archive_material import ArchiveMaterialCommand
from app.application.material.commands.create_material import CreateMaterialCommand
from app.application.material.commands.restore_material import RestoreMaterialCommand
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


def create_material(service: MaterialApplicationService) -> Material:
    return service.create(
        CreateMaterialCommand(
            name="Original Material",
            article="A-001",
            unit="pcs",
            description="Original description",
        ),
        make_user(UserRole.WAREHOUSE),
    )


def test_create_material_allows_warehouse_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)

    assert material.name == "Original Material"
    assert material.article == "A-001"
    assert material.unit == "pcs"
    assert material.description == "Original description"


def test_create_material_rejects_unauthorized_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.create(
            CreateMaterialCommand(
                name="Protected Material",
                article="A-001",
                unit="pcs",
                description="Protected description",
            ),
            make_user(UserRole.TECHNICIAN),
        )


def test_update_material_allows_warehouse_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)

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

    material = create_material(service)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.update(
            UpdateMaterialCommand(
                material_id=material.id,
                name="Unauthorized Update",
            ),
            make_user(UserRole.TECHNICIAN),
        )

    assert material.name == "Original Material"


def test_archive_material_allows_warehouse_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)

    archived = service.archive(
        ArchiveMaterialCommand(material_id=material.id),
        make_user(UserRole.WAREHOUSE),
    )

    assert archived is material
    assert archived.archived is True


def test_archive_material_rejects_unauthorized_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.archive(
            ArchiveMaterialCommand(material_id=material.id),
            make_user(UserRole.TECHNICIAN),
        )

    assert material.archived is False


def test_restore_material_allows_warehouse_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)
    service.archive(
        ArchiveMaterialCommand(material_id=material.id),
        make_user(UserRole.WAREHOUSE),
    )

    restored = service.restore(
        RestoreMaterialCommand(material_id=material.id),
        make_user(UserRole.WAREHOUSE),
    )

    assert restored is material
    assert restored.archived is False


def test_restore_material_rejects_unauthorized_user() -> None:
    repository = FakeMaterialRepository()
    service = MaterialApplicationService(repository)

    material = create_material(service)
    service.archive(
        ArchiveMaterialCommand(material_id=material.id),
        make_user(UserRole.WAREHOUSE),
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.restore(
            RestoreMaterialCommand(material_id=material.id),
            make_user(UserRole.TECHNICIAN),
        )

    assert material.archived is True
