"""
Application exceptions for Device.
"""


class DeviceNotFoundApplicationError(Exception):
    """Device not found application error."""


class DeviceNotAvailableApplicationError(Exception):
    """Device is not available for operation."""


class DeviceNotInWorkApplicationError(Exception):
    """Device is not in work state."""
