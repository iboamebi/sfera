"""
Domain exceptions for Verification.
"""


class VerificationDomainError(Exception):
    """Base verification domain error."""


class InvalidUnsuitableReasonDomainError(VerificationDomainError):
    """Unsuitable verification requires a reason."""
