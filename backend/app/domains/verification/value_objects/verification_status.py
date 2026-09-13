from enum import StrEnum


class VerificationStatus(StrEnum):
    """Lifecycle state of a verification process."""

    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DECIDED = "DECIDED"
