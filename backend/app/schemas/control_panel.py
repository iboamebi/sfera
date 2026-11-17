"""API schemas for the consolidated control-panel overview."""
from pydantic import BaseModel


class KeyCountRead(BaseModel):
    """Count for one status or result key."""
    key: str
    count: int


class EntityStatusCountsRead(BaseModel):
    """Total and active counts with a status distribution."""
    active_count: int
    total_count: int
    by_status: list[KeyCountRead]


class VerificationResultCountsRead(EntityStatusCountsRead):
    """Verification counts split by lifecycle status and result."""
    by_result: list[KeyCountRead]


class CustomerOverviewRead(BaseModel):
    """Customer counts split by archive state."""
    active_count: int
    archived_count: int


class ControlPanelOverviewRead(BaseModel):
    """Aggregate overview for the first control-panel UI slice."""
    orders: EntityStatusCountsRead
    verifications: VerificationResultCountsRead
    customers: CustomerOverviewRead
    instruments: EntityStatusCountsRead
