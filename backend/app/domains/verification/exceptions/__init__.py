"""
Domain exceptions for Verification.
"""


class VerificationDomainError(Exception):
    """Base verification domain error."""


class InvalidUnsuitableReasonDomainError(VerificationDomainError):
    """Unsuitable verification requires a reason."""


class InvalidSuitableValidUntilDomainError(VerificationDomainError):
    """Suitable verification requires a validity date."""


class InvalidVerificationResultStateDomainError(VerificationDomainError):
    """Verification result fields must match the declared result."""
