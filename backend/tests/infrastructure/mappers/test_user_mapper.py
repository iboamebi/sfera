"""
Tests for User mapper.
"""

from uuid import uuid4

from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.infrastructure.mappers.user_mapper import UserMapper
from app.models.user import User as UserModel


def test_user_mapper_to_domain_preserves_authentication_state() -> None:
    user_id = uuid4()
    model = UserModel(
        id=user_id,
        username="test-user",
        password_hash="hash",
        role="operator",
        is_active=True,
        archived=False,
    )

    entity = UserMapper().to_domain(model)

    assert entity.id == user_id
    assert entity.username == "test-user"
    assert entity.password_hash == "hash"
    assert entity.role is UserRole.OPERATOR
    assert entity.archived is False


def test_user_mapper_treats_inactive_user_as_archived() -> None:
    model = UserModel(
        id=uuid4(),
        username="inactive-user",
        password_hash="hash",
        role="operator",
        is_active=False,
        archived=False,
    )

    entity = UserMapper().to_domain(model)

    assert entity.archived is True


def test_user_mapper_to_model_updates_authentication_fields() -> None:
    user_id = uuid4()
    model = UserModel(
        id=user_id,
        username="old-user",
        password_hash="old-hash",
        role="operator",
        is_active=True,
        archived=False,
    )

    entity = User(
        id=user_id,
        username="new-user",
        password_hash="new-hash",
        role=UserRole.ADMIN,
        archived=True,
    )

    result = UserMapper().to_model(entity, model)

    assert result is model
    assert result.username == "new-user"
    assert result.password_hash == "new-hash"
    assert result.role == "admin"
    assert result.archived is True
