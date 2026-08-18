"""
SQLAlchemy implementation of SessionRepository.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session as SQLAlchemySession

from app.domains.auth.entities.session import Session
from app.domains.auth.repositories.session_repository import SessionRepository
from app.infrastructure.mappers.auth_session_mapper import AuthSessionMapper
from app.models.auth_session import AuthSession


class SessionRepositorySQLAlchemy(SessionRepository):
    """SQLAlchemy authentication session repository."""

    def __init__(
        self,
        session: SQLAlchemySession,
    ) -> None:
        self._session = session
        self._mapper = AuthSessionMapper()

    def save(
        self,
        session: Session,
    ) -> Session:
        model = (
            self._session.query(AuthSession)
            .filter(AuthSession.session_id == session.session_id)
            .first()
        )

        if model is None:
            model = AuthSession(id=session.id)
            self._session.add(model)

        self._mapper.to_model(session, model)
        self._session.flush()

        return self._mapper.to_domain(model)

    def get_active(
        self,
        session_id: str,
        now: datetime,
    ) -> Session | None:
        model = (
            self._session.query(AuthSession)
            .filter(
                AuthSession.session_id == session_id,
                AuthSession.revoked.is_(False),
                AuthSession.expires_at > now,
            )
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def revoke(
        self,
        session_id: str,
    ) -> None:
        model = (
            self._session.query(AuthSession)
            .filter(AuthSession.session_id == session_id)
            .first()
        )

        if model is None:
            return

        model.revoked = True
        self._session.flush()

    def revoke_all_for_user(
        self,
        user_id: UUID,
    ) -> None:
        self._session.query(AuthSession).filter(
            AuthSession.user_id == user_id,
            AuthSession.revoked.is_(False),
        ).update(
            {AuthSession.revoked: True},
            synchronize_session=False,
        )
        self._session.flush()
