"""
SQLAlchemy implementation of UserRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.infrastructure.mappers.user_mapper import UserMapper
from app.models.user import User as UserModel


class UserRepositorySQLAlchemy(UserRepository):
    """SQLAlchemy user repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = UserMapper()

    def get_by_id(
        self,
        user_id: UUID,
        include_archived: bool = False,
    ) -> User | None:
        query = self._session.query(UserModel).filter(
            UserModel.id == user_id,
        )

        if not include_archived:
            query = query.filter(
                UserModel.archived.is_(False),
                UserModel.is_active.is_(True),
            )

        model = query.first()

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def get_by_username(
        self,
        username: str,
        include_archived: bool = False,
    ) -> User | None:
        query = self._session.query(UserModel).filter(
            UserModel.username == username,
        )

        if not include_archived:
            query = query.filter(
                UserModel.archived.is_(False),
                UserModel.is_active.is_(True),
            )

        model = query.first()

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def save(
        self,
        user: User,
    ) -> User:
        model = (
            self._session.query(UserModel)
            .filter(
                UserModel.id == user.id,
            )
            .first()
        )

        if model is None:
            model = UserModel(
                id=user.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            user,
            model,
        )

        self._session.flush()

        return self._mapper.to_domain(model)
