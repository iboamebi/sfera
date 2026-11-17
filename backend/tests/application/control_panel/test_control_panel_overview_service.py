from app.application.control_panel.queries.control_panel_overview_service import (
    ControlPanelOverviewService,
)
from app.domains.control_panel.read_models.control_panel_overview_read_model import (
    ArchiveCountReadData,
    ControlPanelOverviewReadData,
    KeyCountReadData,
)
from app.schemas.control_panel import KeyCountRead


class FakeControlPanelReadRepository:
    def __init__(self, data: ControlPanelOverviewReadData) -> None:
        self.data = data

    def get_overview(self) -> ControlPanelOverviewReadData:
        return self.data


def test_overview_calculates_current_counts_from_grouped_source_data() -> None:
    repository = FakeControlPanelReadRepository(
        ControlPanelOverviewReadData(
            order_status_counts=[
                KeyCountReadData(key="NEW", count=2),
                KeyCountReadData(key="IN_WORK", count=3),
                KeyCountReadData(key="COMPLETED", count=5),
            ],
            verification_status_counts=[
                KeyCountReadData(key="CREATED", count=4),
                KeyCountReadData(key="IN_PROGRESS", count=2),
                KeyCountReadData(key="DECIDED", count=7),
            ],
            verification_result_counts=[
                KeyCountReadData(key="SUITABLE", count=5),
                KeyCountReadData(key="UNSUITABLE", count=2),
            ],
            customer_archive_counts=[
                ArchiveCountReadData(archived=False, count=11),
                ArchiveCountReadData(archived=True, count=3),
            ],
            instrument_status_counts=[
                KeyCountReadData(key="AVAILABLE", count=8),
                KeyCountReadData(key="IN_WORK", count=2),
            ],
        )
    )

    result = ControlPanelOverviewService(repository).get_overview()

    assert result.orders.active_count == 5
    assert result.orders.total_count == 10
    assert result.verifications.active_count == 6
    assert result.verifications.total_count == 13
    assert result.verifications.by_result == [
        KeyCountRead(key="SUITABLE", count=5),
        KeyCountRead(key="UNSUITABLE", count=2),
    ]
    assert result.customers.active_count == 11
    assert result.customers.archived_count == 3
    assert result.instruments.total_count == 10
