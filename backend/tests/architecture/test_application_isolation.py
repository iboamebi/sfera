"""
Application layer architecture tests.
"""

from pathlib import Path

from tests.architecture.helpers.imports import (
    get_imports,
    get_python_files,
)

APPLICATION_PATH = Path("app/application")


FORBIDDEN_IMPORTS = (
    "app.infrastructure",
    "app.models",
    "sqlalchemy",
)


def test_application_does_not_depend_on_infrastructure() -> None:
    """Application must not depend on infrastructure layer."""

    for file_path in get_python_files(APPLICATION_PATH):
        imports = get_imports(file_path)

        for imported in imports:
            assert not imported.startswith(
                FORBIDDEN_IMPORTS,
            ), f"{file_path} imports forbidden module {imported}"
