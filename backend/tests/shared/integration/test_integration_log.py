from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.shared.integration.models import IntegrationLog, IntegrationLogStatus


def make_log() -> IntegrationLog:
    return IntegrationLog(
        integration_type="ARSHIN",
        operation="EXPORT",
        created_at=datetime(2026, 11, 17, tzinfo=UTC),
    )


def test_new_integration_log_starts_in_started_status() -> None:
    log = make_log()

    assert log.status == IntegrationLogStatus.STARTED


@pytest.mark.parametrize(
    ("method_name", "expected_status"),
    [
        ("mark_success", IntegrationLogStatus.SUCCESS),
        ("mark_warning", IntegrationLogStatus.WARNING),
        ("mark_error", IntegrationLogStatus.ERROR),
        ("cancel", IntegrationLogStatus.CANCELLED),
    ],
)
def test_started_log_can_be_finalized(
    method_name: str,
    expected_status: IntegrationLogStatus,
) -> None:
    log = make_log()

    getattr(log, method_name)({"result": "done"})

    assert log.status == expected_status
    assert log.response_data == {"result": "done"}


def test_finalized_log_cannot_be_changed() -> None:
    log = make_log()
    log.mark_success()

    with pytest.raises(ValueError, match="already finalized"):
        log.mark_error()


def test_log_preserves_request_and_actor() -> None:
    actor_id = uuid4()
    request_data = {"verification_id": str(uuid4())}

    log = IntegrationLog(
        integration_type="ARSHIN",
        operation="EXPORT",
        request_data=request_data,
        created_by=actor_id,
        created_at=datetime(2026, 11, 17, tzinfo=UTC),
    )

    assert log.request_data == request_data
    assert log.created_by == actor_id
