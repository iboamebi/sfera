from datetime import datetime, timezone
from uuid import uuid4

from app.domains.auth.entities.session import Session
from app.infrastructure.mappers.auth_session_mapper import AuthSessionMapper
from app.models.auth_session import AuthSession


def test_auth_session_mapper_round_trip() -> None:
    session_id = "session-token"
    user_id = uuid4()
    expires_at = datetime(2026, 8, 19, tzinfo=timezone.utc)

    entity = Session(
        id=uuid4(),
        user_id=user_id,
        session_id=session_id,
        expires_at=expires_at,
    )
    model = AuthSession(id=entity.id, created_at=datetime.now(timezone.utc))
    mapper = AuthSessionMapper()

    mapper.to_model(entity, model)
    restored = mapper.to_domain(model)

    assert restored.id == entity.id
    assert restored.user_id == user_id
    assert restored.session_id == session_id
    assert restored.expires_at == expires_at
    assert restored.revoked is False
