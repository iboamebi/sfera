"""Application query service for the consolidated control-panel overview."""
from app.domains.control_panel.repositories.control_panel_read_repository import (
    ControlPanelReadRepository,
)
from app.domains.order.value_objects.order_status import (
    CONFLICTING_INSTRUMENT_ORDER_STATUSES,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.schemas.control_panel import (
    ControlPanelOverviewRead,
    CustomerOverviewRead,
    EntityStatusCountsRead,
    InstrumentOverviewRead,
    KeyCountRead,
    VerificationResultCountsRead,
)


class ControlPanelOverviewService:
    """Builds overview response from aggregate source-domain read data."""

    def __init__(self, repository: ControlPanelReadRepository) -> None:
        self._repository = repository

    def get_overview(self) -> ControlPanelOverviewRead:
        """Return current aggregate counts for the first control-panel slice."""
        data = self._repository.get_overview()
        order_counts = {item.key: item.count for item in data.order_status_counts}
        verification_counts = {
            item.key: item.count for item in data.verification_status_counts
        }
        customer_counts = {
            item.archived: item.count for item in data.customer_archive_counts
        }
        instrument_counts = {
            item.key: item.count for item in data.instrument_status_counts
        }
        active_order_statuses = {
            status.value for status in CONFLICTING_INSTRUMENT_ORDER_STATUSES
        }
        active_verification_statuses = {
            VerificationStatus.CREATED.value,
            VerificationStatus.IN_PROGRESS.value,
        }

        return ControlPanelOverviewRead(
            orders=EntityStatusCountsRead(
                active_count=sum(
                    count for key, count in order_counts.items()
                    if key in active_order_statuses
                ),
                total_count=sum(order_counts.values()),
                by_status=[
                    KeyCountRead(key=item.key, count=item.count)
                    for item in data.order_status_counts
                ],
            ),
            verifications=VerificationResultCountsRead(
                active_count=sum(
                    count for key, count in verification_counts.items()
                    if key in active_verification_statuses
                ),
                total_count=sum(verification_counts.values()),
                by_status=[
                    KeyCountRead(key=item.key, count=item.count)
                    for item in data.verification_status_counts
                ],
                by_result=[
                    KeyCountRead(key=item.key, count=item.count)
                    for item in data.verification_result_counts
                ],
            ),
            customers=CustomerOverviewRead(
                active_count=customer_counts.get(False, 0),
                archived_count=customer_counts.get(True, 0),
            ),
            instruments=InstrumentOverviewRead(
                total_count=sum(instrument_counts.values()),
                by_status=[
                    KeyCountRead(key=item.key, count=item.count)
                    for item in data.instrument_status_counts
                ],
            ),
        )
