"""Application service for user administration."""

import secrets
from uuid import uuid4

from app.shared.password_hasher import PasswordHasher
from app.application.authorization.authorization import require_role
from app.application.user.commands.archive_user import ArchiveUserCommand
from app.application.user.commands.change_user_role import ChangeUserRoleCommand
from app.application.user.commands.create_user import CreateUserCommand
from app.application.user.commands.restore_user import RestoreUserCommand
from app.application.user.commands.set_user_active import SetUserActiveCommand
from app.application.user.exceptions import (
    LastActiveAdministratorApplicationError,
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class UserAdministrationApplicationService:
    """Coordinates administrator-only user management use cases."""

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher
        self._uow = uow

    def get_all(self, user: User, include_archived: bool = False) -> list[User]:
        """List users for an administrator."""
        require_role(user, UserRole.ADMIN)
        return self._repository.get_all(include_archived=include_archived)

    def change_role(self, command: ChangeUserRoleCommand, actor: User) -> User:
        """Change a user's role as an administrator."""
        require_role(actor, UserRole.ADMIN)

        with self._uow:
            if command.role is not UserRole.ADMIN:
                users = self._repository.get_all_for_update()
                user = next((item for item in users if item.id == command.user_id), None)
            else:
                user = self._repository.get_by_id(
                    command.user_id,
                    include_archived=True,
                )
            if user is None:
                raise UserNotFoundApplicationError

            if (
                command.role is not UserRole.ADMIN
                and user.role is UserRole.ADMIN
                and user.is_active
                and not user.archived
            ):
                active_admins = [
                    item for item in users
                    if item.role is UserRole.ADMIN and item.is_active and not item.archived
                ]
                if len(active_admins) <= 1:
                    raise LastActiveAdministratorApplicationError

            user.change_role(command.role)
            return self._repository.save(user)

    def set_active(self, command: SetUserActiveCommand, actor: User) -> User:
        """Activate or deactivate a non-archived account."""
        require_role(actor, UserRole.ADMIN)

        with self._uow:
            if command.is_active:
                user = self._repository.get_by_id(
                    command.user_id,
                    include_archived=True,
                )
                users = []
            else:
                users = self._repository.get_all_for_update()
                user = next((item for item in users if item.id == command.user_id), None)
            if user is None or user.archived:
                raise UserNotFoundApplicationError

            if command.is_active:
                user.activate()
            else:
                if user.role is UserRole.ADMIN and user.is_active:
                    active_admins = [
                        item for item in users
                        if item.role is UserRole.ADMIN and item.is_active and not item.archived
                    ]
                    if len(active_admins) <= 1:
                        raise LastActiveAdministratorApplicationError
                user.deactivate()

            return self._repository.save(user)

    def archive(self, command: ArchiveUserCommand, actor: User) -> User:
        """Archive an existing account while preserving its history."""
        require_role(actor, UserRole.ADMIN)

        with self._uow:
            users = self._repository.get_all_for_update()
            user = next((item for item in users if item.id == command.user_id), None)
            if user is None or user.archived:
                raise UserNotFoundApplicationError

            if user.role is UserRole.ADMIN and user.is_active:
                active_admins = [
                    item for item in users
                    if item.role is UserRole.ADMIN and item.is_active and not item.archived
                ]
                if len(active_admins) <= 1:
                    raise LastActiveAdministratorApplicationError

            user.archive()
            return self._repository.save(user)

    def restore(self, command: RestoreUserCommand, actor: User) -> User:
        """Restore an archived account."""
        require_role(actor, UserRole.ADMIN)

        with self._uow:
            user = self._repository.get_by_id(
                command.user_id,
                include_archived=True,
            )
            if user is None or not user.archived:
                raise UserNotFoundApplicationError

            user.restore()
            return self._repository.save(user)

    def create(self, command: CreateUserCommand, actor: User) -> tuple[User, str]:
        """Create an account and return its temporary password exactly once."""
        require_role(actor, UserRole.ADMIN)

        if (
            self._repository.get_by_username(
                command.username,
                include_archived=True,
            )
            is not None
        ):
            raise UserAlreadyExistsApplicationError

        temporary_password = secrets.token_urlsafe(18)
        user = User(
            id=uuid4(),
            username=command.username,
            password_hash=self._password_hasher.hash(temporary_password),
            role=command.role,
            must_change_password=True,
        )

        with self._uow:
            created_user = self._repository.save(user)

        return created_user, temporary_password
