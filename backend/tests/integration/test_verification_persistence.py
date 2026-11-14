"""Real PostgreSQL persistence regression tests.

Run only against the explicitly configured disposable integration database.
"""

import os
from datetime import UTC, date, datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

import app.db.model_registry  # noqa: F401
from app.application.verification.commands.start_verification import (
    StartVerificationCommand,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.user.entities.user import User as DomainUser
from app.domains.user.value_objects.user_role import UserRole
from app.infrastructure.audit.audit_operation_repository import (
    AuditOperationRepositorySQLAlchemy,
)
from app.infrastructure.audit.audit_repository import AuditRepositorySQLAlchemy
from app.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.order.order_repository import OrderRepositorySQLAlchemy
from app.infrastructure.verification.verification_repository import (
    VerificationRepositorySQLAlchemy,
)
from app.models.customer import Customer
from app.models.instrument import Instrument
from app.models.instrument_type import InstrumentType
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.verification import (
    Verification,
    VerificationStatus,
    VerificationType,
)


def _integration_database_url() -> str:
    url = os.getenv("SFERA_INTEGRATION_DATABASE_URL")
    if not url:
        pytest.skip("SFERA_INTEGRATION_DATABASE_URL is not configured")

    parsed = make_url(url)
    if (
        parsed.drivername != "postgresql+psycopg2"
        or parsed.host != "127.0.0.1"
        or parsed.port != 55432
        or parsed.database != "sfera_test"
    ):
        pytest.fail(
            "Refusing to run integration test outside "
            "127.0.0.1:55432/sfera_test"
        )
    return url


def test_starting_one_verification_preserves_all_order_items_and_verifications():
    engine = create_engine(_integration_database_url())
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    try:
        with Session(engine) as check_session:
            revision = check_session.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one()
            assert revision == "c2e5f7a9b310"

        customer_id = uuid4()
        instrument_type_id = uuid4()
        first_instrument_id = uuid4()
        second_instrument_id = uuid4()
        order_id = uuid4()
        first_item_id = uuid4()
        second_item_id = uuid4()
        first_verification_id = uuid4()
        second_verification_id = uuid4()
        user_id = uuid4()
        now = datetime.now(UTC)

        with session_factory() as seed_session:
            seed_session.add(
                Customer(id=customer_id, name="Persistence regression customer")
            )
            seed_session.add(
                InstrumentType(id=instrument_type_id, name="Integration test type")
            )
            seed_session.add_all(
                [
                    Instrument(
                        id=first_instrument_id,
                        customer_id=customer_id,
                        instrument_type_id=instrument_type_id,
                        serial_number=f"IT-{first_instrument_id}",
                    ),
                    Instrument(
                        id=second_instrument_id,
                        customer_id=customer_id,
                        instrument_type_id=instrument_type_id,
                        serial_number=f"IT-{second_instrument_id}",
                    ),
                ]
            )
            seed_session.flush()
            seed_session.add(
                Order(
                    id=order_id,
                    number=f"IT-{order_id}",
                    customer_id=customer_id,
                    received_at=now,
                    status=OrderStatus.REGISTERED,
                    order_items=[
                        OrderItem(
                            id=first_item_id,
                            instrument_id=first_instrument_id,
                            line_number=1,
                            quantity=1,
                            requested_operations=[],
                        ),
                        OrderItem(
                            id=second_item_id,
                            instrument_id=second_instrument_id,
                            line_number=2,
                            quantity=1,
                            requested_operations=[],
                        ),
                    ],
                )
            )
            seed_session.flush()
            seed_session.add_all(
                [
                    Verification(
                        id=first_verification_id,
                        order_item_id=first_item_id,
                        instrument_id=first_instrument_id,
                        verification_date=date(2026, 11, 14),
                        created_at=now,
                        status=VerificationStatus.CREATED,
                        verification_type=VerificationType.PERIODIC,
                    ),
                    Verification(
                        id=second_verification_id,
                        order_item_id=second_item_id,
                        instrument_id=second_instrument_id,
                        verification_date=date(2026, 11, 14),
                        created_at=now,
                        status=VerificationStatus.CREATED,
                        verification_type=VerificationType.PERIODIC,
                    ),
                ]
            )
            seed_session.commit()

        with session_factory() as service_session:
            service = VerificationApplicationService(
                VerificationRepositorySQLAlchemy(service_session),
                OrderRepositorySQLAlchemy(service_session),
                SqlAlchemyUnitOfWork(service_session, event_dispatcher=Mock()),
                AuditOperationRepositorySQLAlchemy(service_session),
                AuditRepositorySQLAlchemy(service_session),
            )
            service.start(
                StartVerificationCommand(verification_id=first_verification_id),
                DomainUser(
                    id=user_id,
                    username="integration-metrologist",
                    password_hash="not-a-login",
                    role=UserRole.METROLOGIST,
                ),
            )

        with session_factory() as verification_session:
            persisted_order = (
                verification_session.query(Order)
                .filter(Order.id == order_id)
                .one()
            )
            persisted_verifications = (
                verification_session.query(Verification)
                .filter(
                    Verification.order_item_id.in_([first_item_id, second_item_id])
                )
                .all()
            )
            statuses = {item.id: item.status for item in persisted_verifications}

            assert {item.id for item in persisted_order.order_items} == {
                first_item_id,
                second_item_id,
            }
            assert statuses == {
                first_verification_id: VerificationStatus.IN_PROGRESS,
                second_verification_id: VerificationStatus.CREATED,
            }
            assert persisted_order.status == OrderStatus.IN_WORK
    finally:
        engine.dispose()
