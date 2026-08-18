from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.customer import router
from app.api.security.csrf import require_csrf


def _route(path: str, method: str) -> APIRoute:
    for route in router.routes:
        if (
            isinstance(route, APIRoute)
            and route.path == path
            and method in route.methods
        ):
            return route
    raise AssertionError(f"Route not found: {method} {path}")


def _dependency_calls(route: APIRoute) -> set[object]:
    return {dependency.call for dependency in route.dependant.dependencies}


def test_customer_reads_do_not_require_authentication() -> None:
    assert get_current_user not in _dependency_calls(
        _route("/customers/", "GET"),
    )
    assert get_current_user not in _dependency_calls(
        _route("/customers/{customer_id}", "GET"),
    )


def test_customer_mutations_require_authentication_and_csrf() -> None:
    for method, path in (
        ("POST", "/customers/"),
        ("PATCH", "/customers/{customer_id}"),
        ("DELETE", "/customers/{customer_id}"),
    ):
        dependencies = _dependency_calls(_route(path, method))
        assert get_current_user in dependencies
        assert require_csrf in dependencies
