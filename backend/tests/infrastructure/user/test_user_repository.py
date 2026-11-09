from uuid import uuid4

from app.domains.user.value_objects.user_role import UserRole
from app.infrastructure.user.user_repository import UserRepositorySQLAlchemy
from app.models.user import User as UserModel


class FakeQuery:
    def __init__(self, models: list[UserModel]) -> None:
        self.models = models
        self.ordered = False

    def filter(self, *conditions: object) -> "FakeQuery":
        return self

    def order_by(self, *columns: object) -> "FakeQuery":
        self.ordered = True
        return self

    def all(self) -> list[UserModel]:
        return self.models


class FakeSession:
    def __init__(self, models: list[UserModel]) -> None:
        self.models = models
        self.query_result = FakeQuery(models)

    def query(self, model: type[UserModel]) -> FakeQuery:
        return self.query_result


def test_get_all_returns_inactive_users_for_administration() -> None:
    active = UserModel(
        id=uuid4(),
        username="active",
        password_hash="hash",
        role=UserRole.OPERATOR.value,
        is_active=True,
        archived=False,
        must_change_password=False,
    )
    inactive = UserModel(
        id=uuid4(),
        username="inactive",
        password_hash="hash",
        role=UserRole.TECHNICIAN.value,
        is_active=False,
        archived=False,
        must_change_password=True,
    )
    session = FakeSession([active, inactive])

    result = UserRepositorySQLAlchemy(session).get_all()

    assert [user.username for user in result] == ["active", "inactive"]
    assert result[1].is_active is False
    assert result[1].must_change_password is True
    assert session.query_result.ordered is True
