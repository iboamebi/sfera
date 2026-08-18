"""
Secure session token generator implementation.
"""

import secrets

from app.domains.auth.services.session_token_generator import SessionTokenGenerator


class SecureSessionTokenGenerator(SessionTokenGenerator):
    """Generate cryptographically secure server-side session identifiers."""

    def generate(self) -> str:
        """Generate a URL-safe random session identifier."""

        return secrets.token_urlsafe(32)
