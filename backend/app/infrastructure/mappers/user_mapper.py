"""
User domain/model mapper.
"""

from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.user import User as UserModel


class UserMapper(
    BaseMapper[
        User,
        UserModel,
    ],
):
    """Maps User between domain entity and SQLAlchemy model."""

    def to_domain(
        self,
        model: UserModel,
    ) -> User:
        """Convert ORM model to domain entity."""

        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password_hash,
            role=UserRole(model.role),
            archived=model.archived,
            is_active=model.is_active,
            must_change_password=model.must_change_password,
        )

    def to_model(
        self,
        entity: User,
        model: UserModel,
    ) -> UserModel:
        """Convert User between domain entity and ORM model."""

        model.username = entity.username
        model.password_hash = entity.password_hash
        model.role = entity.role.value
        model.archived = entity.archived
        model.is_active = entity.is_active
        model.must_change_password = entity.must_change_password

        return model
