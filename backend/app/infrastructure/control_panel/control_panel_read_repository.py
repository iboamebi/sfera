"""SQLAlchemy aggregate read repository for the control panel."""
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domains.control_panel.read_models.control_panel_overview_read_model import (
    ArchiveCountReadData,
    ControlPanelOverviewReadData,
    KeyCountReadData,
)
from app.domains.control_panel.repositories.control_panel_read_repository import (
    ControlPanelReadRepository,
)
from app.models.customer import Customer
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.verification import Verification


class ControlPanelReadRepositorySQLAlchemy(ControlPanelReadRepository):
    """Reads grouped counts directly from source tables."""

    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _key(value: object) -> str:
        return value.value if hasattr(value, "value") else str(value)

    def get_overview(self) -> ControlPanelOverviewReadData:
        order_rows = (
            self._session.query(Order.status, func.count(Order.id))
            .filter(Order.archived.is_(False))
            .group_by(Order.status).all()
        )
        verification_status_rows = (
            self._session.query(Verification.status, func.count(Verification.id))
            .filter(Verification.archived.is_(False))
            .group_by(Verification.status).all()
        )
        verification_result_rows = (
            self._session.query(Verification.result, func.count(Verification.id))
            .filter(
                Verification.archived.is_(False),
                Verification.result.is_not(None),
            )
            .group_by(Verification.result).all()
        )
        customer_rows = (
            self._session.query(Customer.archived, func.count(Customer.id))
            .group_by(Customer.archived).all()
        )
        instrument_rows = (
            self._session.query(Instrument.device_status, func.count(Instrument.id))
            .group_by(Instrument.device_status).all()
        )

        return ControlPanelOverviewReadData(
            order_status_counts=[
                KeyCountReadData(key=self._key(key), count=count)
                for key, count in order_rows
            ],
            verification_status_counts=[
                KeyCountReadData(key=self._key(key), count=count)
                for key, count in verification_status_rows
            ],
            verification_result_counts=[
                KeyCountReadData(key=self._key(key), count=count)
                for key, count in verification_result_rows
            ],
            customer_archive_counts=[
                ArchiveCountReadData(archived=archived, count=count)
                for archived, count in customer_rows
            ],
            instrument_status_counts=[
                KeyCountReadData(key=self._key(key), count=count)
                for key, count in instrument_rows
            ],
        )
