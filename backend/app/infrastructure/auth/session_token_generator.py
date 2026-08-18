"""
Secure session token generator implementation.
"""

import secrets


class SecureSessionTokenGenerator:
    """Generate cryptographically secure server-side session identifiers."""

    def generate(self) -> str:
        """Generate a URL-safe random session identifier."""

        return secrets.token_urlsafe(32)
