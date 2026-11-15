from datetime import date, datetime, UTC
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.auth import require_password_change_completed
from app.core.dependencies.services import get_verification_read_service
from app.main import app
from app.schemas.verification import VerificationListRead
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import (
    VerificationType,
)


class FakeVerificationReadService:
    def __init__(self, result: list[VerificationListRead]) -> None:
        self.result = result

    def list(self) -> list[VerificationListRead]:
        return self.result


def test_list_verifications_returns_read_models():
    verification = VerificationListRead(
        id=uuid4(),
        order_item_id=uuid4(),
        order_id=uuid4(),
        order_number="ORD-001",
        customer_id=uuid4(),
        customer_name="ООО Клиент",
        instrument_id=uuid4(),
        instrument_name="Манометр",
        instrument_type_id=uuid4(),
        instrument_type_name="Манометры",
        serial_number="12345",
        verification_date=date(2026, 11, 14),
        verification_type=VerificationType.PERIODIC,
        status=VerificationStatus.DECIDED,
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 11, 13),
        created_at=datetime(2026, 11, 14, 11, 0),
        started_at=datetime(2026, 11, 14, 9, 0),
        decision_at=datetime(2026, 11, 14, 11, 0),
        archived=False,
    )

    app.dependency_overrides[get_verification_read_service] = (
        lambda: FakeVerificationReadService([verification])
    )
    app.dependency_overrides[require_password_change_completed] = lambda: None

    try:
        response = TestClient(app).get("/verifications/")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [verification.model_dump(mode="json")]
