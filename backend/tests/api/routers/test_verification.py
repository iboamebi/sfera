from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.authorization.authorization import AuthorizationError
from app.application.verification.exceptions import (
    VerificationInstrumentRequiredApplicationError,
    VerificationOrderItemNotFoundApplicationError,
)
from app.core.dependencies.services import get_verification_service
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.main import app


class FakeVerificationService:
    def __init__(
        self,
        result: Verification | Exception,
    ) -> None:
        self.result = result

    def create(self, command, user):
        if isinstance(self.result, Exception):
            raise self.result

        return self.result


def make_user() -> User:
    return User(
        id=uuid4(),
        username="metrologist",
        password_hash="hash",
        role=UserRole.METROLOGIST,
    )


def make_payload(order_item_id: str) -> dict[str, str]:
    return {
        "order_item_id": order_item_id,
        "verification_date": "2026-09-05",
        "result": "SUITABLE",
        "valid_until": "2027-09-05",
        "methodology": "MI 123",
    }


def make_client(service: FakeVerificationService) -> TestClient:
    app.dependency_overrides[get_current_user] = make_user
    app.dependency_overrides[get_verification_service] = lambda: service
    app.dependency_overrides[require_csrf] = lambda: None

    return TestClient(app)


def clear_overrides() -> None:
    app.dependency_overrides.clear()


def test_create_verification_returns_created_verification():
    order_item_id = uuid4()
    verification = Verification(
        id=uuid4(),
        order_item_id=order_item_id,
        instrument_id=uuid4(),
        verification_date=date(2026, 9, 5),
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 9, 5),
        methodology="MI 123",
    )
    client = make_client(FakeVerificationService(verification))

    try:
        response = client.post(
            "/verifications",
            json=make_payload(str(order_item_id)),
        )
    finally:
        clear_overrides()

    assert response.status_code == 200
    assert response.json() == {
        "order_item_id": str(order_item_id),
        "verification_date": "2026-09-05",
        "valid_until": "2027-09-05",
        "result": "SUITABLE",
        "unsuitable_reason": None,
        "methodology": "MI 123",
        "id": str(verification.id),
        "archived": False,
    }


def test_create_verification_returns_not_found_for_unknown_order_item():
    client = make_client(
        FakeVerificationService(
            VerificationOrderItemNotFoundApplicationError(),
        )
    )

    try:
        response = client.post(
            "/verifications",
            json=make_payload(str(uuid4())),
        )
    finally:
        clear_overrides()

    assert response.status_code == 404
    assert response.json() == {"detail": "Order item not found"}


def test_create_verification_requires_concrete_instrument():
    client = make_client(
        FakeVerificationService(
            VerificationInstrumentRequiredApplicationError(),
        )
    )

    try:
        response = client.post(
            "/verifications",
            json=make_payload(str(uuid4())),
        )
    finally:
        clear_overrides()

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Verification requires a concrete instrument",
    }


def test_create_verification_returns_forbidden_for_unauthorized_user():
    client = make_client(FakeVerificationService(AuthorizationError()))

    try:
        response = client.post(
            "/verifications",
            json=make_payload(str(uuid4())),
        )
    finally:
        clear_overrides()

    assert response.status_code == 403
