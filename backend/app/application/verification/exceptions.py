class VerificationNotFoundApplicationError(Exception):
    """Verification not found."""


class VerificationOrderItemNotFoundApplicationError(Exception):
    """Verification order item not found."""


class VerificationInstrumentRequiredApplicationError(Exception):
    """Verification requires a concrete instrument."""


class VerificationCannotBeStartedApplicationError(Exception):
    """Verification cannot be started from its current state."""


class VerificationCannotBeCancelledApplicationError(Exception):
    """Verification cannot be cancelled from its current state."""


class VerificationCancellationReasonRequiredApplicationError(Exception):
    """Cancellation reason is required."""


class VerificationAlreadyActiveApplicationError(Exception):
    """An unarchived verification is already active for this order item."""
