"""Application errors for user administration."""


class UserAlreadyExistsApplicationError(Exception):
    """Raised when a username is already reserved by an existing account."""
