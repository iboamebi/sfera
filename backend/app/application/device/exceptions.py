"""
Application exceptions for Device.
"""


class DeviceNotFoundApplicationError(Exception):
    """Device not found application error."""


class DeviceNotAvailableApplicationError(Exception):
    """Device is not available for operation."""


class DeviceNotInWorkApplicationError(Exception):
    """Device is not in work state."""


class InstrumentTypeNotFoundApplicationError(Exception):
    """Instrument type was not found."""


class CustomerNotFoundApplicationError(Exception):
    """Customer was not found."""


class SiteNotFoundApplicationError(Exception):
    """Site was not found."""


class SiteCustomerMismatchApplicationError(Exception):
    """Site does not belong to the device customer."""


class DuplicateDeviceSerialNumberApplicationError(Exception):
    """Serial number already exists for this customer and instrument type."""
