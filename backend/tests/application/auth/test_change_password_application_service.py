from uuid import uuid4

import pytest

from app.application.auth.commands.change_password import ChangePasswordCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.ports.password_hasher import PasswordHasher
from app.application.auth.services.change_password_application_service import (
    ChangePasswordApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.repositories.user_repository import UserRepository
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password == "temporary-password" and password_hash == "temporary-hash"


class FakeUserRepository(UserRepository):
    def __init__(self, user: User | None) -> None:
        self.user = user
        self.saved = False

    def get_by_id(
        self,
        user_id,
        include_archived: bool = False,
    ) -> User | None:
        if self.user is None or self.user.id != user_id:
            return None
        if not include_archived and (self.user.archived or not self.user.is_active):
            return None
        return self.user

    def get_by_username(
        self,
        username,
        include_archived: bool = False,
    ) -> User | None:
        raise NotImplementedError

    def save(self, user: User) -> User:
        self.saved = True
        self.user = user
        return user


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def register_aggregate(self, aggregate, operation_id=None) -> None:
        pass


def test_change_password_hashes_password_and_clears_first_login_flag() -> None:
    user = User(
        id=uuid4(),
        username="alice",
        password_hash="temporary-hash",
        must_change_password=True,
    )
    repository = FakeUserRepository(user)
    uow = FakeUnitOfWork()
    service = ChangePasswordApplicationService(
        repository,
        FakePasswordHasher(),
        uow,
    )

    service.change(
        ChangePasswordCommand(
            user_id=user.id,
            current_password="temporary-password",
            new_password="new-password",
        )
    )

    assert user.password_hash == "hashed:new-password"
    assert user.must_change_password is False
    assert repository.saved is True
    assert uow.committed is True


def test_change_password_rejects_wrong_current_password() -> None:
    user = User(id=uuid4(), username="alice", password_hash="temporary-hash")
    repository = FakeUserRepository(user)
    uow = FakeUnitOfWork()
    service = ChangePasswordApplicationService(repository, FakePasswordHasher(), uow)

    with pytest.raises(AuthenticationFailedApplicationError):
        service.change(
            ChangePasswordCommand(
                user_id=user.id,
                current_password="wrong-password",
                new_password="new-password",
            )
        )

    assert repository.saved is False
    assert uow.committed is False


def test_change_password_rejects_unknown_user() -> None:
    service = ChangePasswordApplicationService(
        FakeUserRepository(None), FakePasswordHasher(), FakeUnitOfWork()
    )

    with pytest.raises(AuthenticationFailedApplicationError):
        service.change(
            ChangePasswordCommand(
                user_id=uuid4(),
                current_password="temporary-password",
                new_password="new-password",
            )
        )
