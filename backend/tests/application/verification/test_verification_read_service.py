from datetime import UTC, date, datetime
from uuid import uuid4

from app.application.verification.queries.verification_read_service import (
    VerificationReadService,
)
from app.domains.verification.read_models.verification_read_models import (
    VerificationListReadData,
)
from app.domains.verification.repositories.verification_read_repository import (
    VerificationReadRepository,
)
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import (
    VerificationType,
)


class FakeVerificationReadRepository(VerificationReadRepository):
    def __init__(self, records: list[VerificationListReadData]) -> None:
        self.records = records

    def list(self) -> list[VerificationListReadData]:
        return self.records


def test_verification_read_service_maps_list_records():
    verification_id = uuid4()
    order_item_id = uuid4()
    order_id = uuid4()
    customer_id = uuid4()
    instrument_id = uuid4()
    instrument_type_id = uuid4()
    created_at = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)

    record = VerificationListReadData(
        id=verification_id,
        order_item_id=order_item_id,
        order_id=order_id,
        order_number="ORD-001",
        customer_id=customer_id,
        customer_name="ООО Клиент",
        instrument_id=instrument_id,
        instrument_name="Манометр",
        instrument_type_id=instrument_type_id,
        instrument_type_name="Манометры",
        serial_number="12345",
        verification_date=date(2026, 11, 14),
        verification_type=VerificationType.PERIODIC,
        status=VerificationStatus.DECIDED,
        result=VerificationResult.SUITABLE,
        valid_until=date(2027, 11, 13),
        created_at=created_at,
        started_at=datetime(2026, 11, 14, 9, 0, tzinfo=UTC),
        decision_at=datetime(2026, 11, 14, 11, 0, tzinfo=UTC),
        archived=False,
    )

    result = VerificationReadService(
        FakeVerificationReadRepository([record]),
    ).list()

    assert len(result) == 1
    assert result[0].id == verification_id
    assert result[0].order_number == "ORD-001"
    assert result[0].customer_name == "ООО Клиент"
    assert result[0].instrument_name == "Манометр"
    assert result[0].status == VerificationStatus.DECIDED
    assert result[0].result == VerificationResult.SUITABLE
    assert result[0].valid_until == date(2027, 11, 13)
