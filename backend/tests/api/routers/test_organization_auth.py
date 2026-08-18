from fastapi import Depends

from app.api.dependencies.auth import get_current_user
from app.api.routers.organization import create_organization, update_organization
from app.api.security.csrf import require_csrf


def test_create_organization_requires_authentication_and_csrf() -> None:
    dependencies = create_organization.__dependencies__

    assert any(dependency.call is get_current_user for dependency in dependencies)
    assert any(dependency.call is require_csrf for dependency in dependencies)


def test_update_organization_requires_authentication_and_csrf() -> None:
    dependencies = update_organization.__dependencies__

    assert any(dependency.call is get_current_user for dependency in dependencies)
    assert any(dependency.call is require_csrf for dependency in dependencies)
