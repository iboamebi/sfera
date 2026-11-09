"""Application service: change the authenticated user's password."""

from app.application.auth.commands.change_password import ChangePasswordCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.domains.user.repositories.user_repository import UserRepository
from app.shared.password_hasher import PasswordHasher
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class ChangePasswordApplicationService:
    """Change a user's password and clear the first-login requirement."""

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher
        self._uow = uow

    def change(self, command: ChangePasswordCommand) -> None:
        """Verify the current password and persist its replacement."""

        user = self._repository.get_by_id(command.user_id)
        if user is None or user.archived or not user.is_active:
            raise AuthenticationFailedApplicationError

        if not self._password_hasher.verify(
            command.current_password,
            user.password_hash,
        ):
            raise AuthenticationFailedApplicationError

        with self._uow:
            user.change_password(self._password_hasher.hash(command.new_password))
            self._repository.save(user)
