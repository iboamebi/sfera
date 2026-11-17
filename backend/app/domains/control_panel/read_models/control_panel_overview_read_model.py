"""Read models for the consolidated control-panel overview."""
from dataclasses import dataclass


@dataclass(frozen=True)
class KeyCountReadData:
    """Count grouped by a source-domain key."""
    key: str
    count: int


@dataclass(frozen=True)
class ArchiveCountReadData:
    """Customer count grouped by its archive flag."""
    archived: bool
    count: int


@dataclass(frozen=True)
class ControlPanelOverviewReadData:
    """Aggregated counts from source business modules."""
    order_status_counts: list[KeyCountReadData]
    verification_status_counts: list[KeyCountReadData]
    verification_result_counts: list[KeyCountReadData]
    customer_archive_counts: list[ArchiveCountReadData]
    instrument_status_counts: list[KeyCountReadData]
