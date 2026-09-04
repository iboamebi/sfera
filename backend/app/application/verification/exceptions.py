class VerificationNotFoundApplicationError(Exception):
    """Verification not found."""


class VerificationOrderItemNotFoundApplicationError(Exception):
    """Verification order item not found."""


class VerificationInstrumentRequiredApplicationError(Exception):
    """Verification requires a concrete instrument."""
