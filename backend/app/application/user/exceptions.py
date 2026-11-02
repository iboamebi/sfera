"""Application errors for user administration."""


class UserAlreadyExistsApplicationError(Exception):
    """Raised when a username is already reserved by an existing account."""


class UserNotFoundApplicationError(Exception):
    """Raised when the requested user account does not exist."""
