"""
Dependency direction architecture tests.
"""

from pathlib import Path

from tests.architecture.helpers.imports import (
    get_imports,
    get_python_files,
)

LAYER_PATHS = {
    "api": Path("app/api"),
    "application": Path("app/application"),
    "domains": Path("app/domains"),
    "infrastructure": Path("app/infrastructure"),
}


FORBIDDEN_DEPENDENCIES = {
    "domains": (
        "app.api",
        "app.application",
        "app.infrastructure",
    ),
    "application": (
        "app.api",
        "app.infrastructure",
    ),
    "infrastructure": (
        "app.api",
        "app.application",
    ),
}


def test_dependency_direction() -> None:
    """Verify clean architecture dependency direction."""

    for layer, forbidden in FORBIDDEN_DEPENDENCIES.items():
        for file_path in get_python_files(
            LAYER_PATHS[layer],
        ):
            imports = get_imports(file_path)

            for imported in imports:
                assert not imported.startswith(
                    forbidden,
                ), f"{file_path} violates dependency direction: {imported}"
