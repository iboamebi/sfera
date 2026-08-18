"""
Authentication session domain/model mapper.
"""

from app.domains.auth.entities.session import Session
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.auth_session import AuthSession


class AuthSessionMapper(BaseMapper[Session, AuthSession]):
    """Maps authentication sessions between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: AuthSession,
    ) -> Session:
        """Convert ORM model to domain entity."""

        return Session(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            expires_at=model.expires_at,
            revoked=model.revoked,
        )

    def to_model(
        self,
        entity: Session,
        model: AuthSession,
    ) -> AuthSession:
        """Convert domain entity to ORM model."""

        model.user_id = entity.user_id
        model.session_id = entity.session_id
        model.expires_at = entity.expires_at
        model.revoked = entity.revoked

        return model
