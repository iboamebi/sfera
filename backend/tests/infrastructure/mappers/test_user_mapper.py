"""
Tests for User mapper.
"""

from uuid import uuid4

from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.infrastructure.mappers.user_mapper import UserMapper
from app.models.user import User as UserModel


def test_user_mapper_to_domain_preserves_account_state() -> None:
    user_id = uuid4()
    model = UserModel(
        id=user_id,
        username="test-user",
        password_hash="hash",
        role="operator",
        is_active=True,
        archived=False,
        must_change_password=True,
    )

    entity = UserMapper().to_domain(model)

    assert entity.id == user_id
    assert entity.username == "test-user"
    assert entity.password_hash == "hash"
    assert entity.role is UserRole.OPERATOR
    assert entity.archived is False
    assert entity.is_active is True
    assert entity.must_change_password is True


def test_user_mapper_keeps_inactive_and_archived_states_separate() -> None:
    model = UserModel(
        id=uuid4(),
        username="inactive-user",
        password_hash="hash",
        role="operator",
        is_active=False,
        archived=False,
        must_change_password=False,
    )

    entity = UserMapper().to_domain(model)

    assert entity.archived is False
    assert entity.is_active is False


def test_user_mapper_to_model_updates_authentication_fields() -> None:
    user_id = uuid4()
    model = UserModel(
        id=user_id,
        username="old-user",
        password_hash="old-hash",
        role="operator",
        is_active=True,
        archived=False,
        must_change_password=False,
    )

    entity = User(
        id=user_id,
        username="new-user",
        password_hash="new-hash",
        role=UserRole.ADMIN,
        archived=True,
        is_active=False,
        must_change_password=True,
    )

    result = UserMapper().to_model(entity, model)

    assert result is model
    assert result.username == "new-user"
    assert result.password_hash == "new-hash"
    assert result.role == "admin"
    assert result.archived is True
    assert result.is_active is False
    assert result.must_change_password is True
