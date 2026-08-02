"""
Domain exceptions for Device.
"""


class DeviceDomainError(Exception):
    """Base device domain error."""


class DeviceNotAvailableDomainError(DeviceDomainError):
    """Device cannot be connected because it is unavailable."""


class DeviceNotInWorkDomainError(DeviceDomainError):
    """Device cannot be disconnected because it is not in work."""


class InvalidSerialNumberDomainError(DeviceDomainError):
    """Serial number is invalid."""
