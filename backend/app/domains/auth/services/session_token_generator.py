"""
Session token generator interface.
"""

from abc import ABC, abstractmethod


class SessionTokenGenerator(ABC):
    """Abstract secure session token generator."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a cryptographically secure session token."""

        raise NotImplementedError
