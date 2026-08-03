"""
API layer architecture tests.
"""

from pathlib import Path

from tests.architecture.helpers.imports import (
    get_imports,
    get_python_files,
)

API_PATH = Path("app/api")


FORBIDDEN_IMPORTS = (
    "app.infrastructure",
    "app.models",
    "sqlalchemy",
)


def test_api_does_not_depend_on_lower_layers() -> None:
    """API must not depend on infrastructure or ORM."""

    for file_path in get_python_files(API_PATH):
        imports = get_imports(file_path)

        for imported in imports:
            assert not imported.startswith(
                FORBIDDEN_IMPORTS,
            ), f"{file_path} imports forbidden module {imported}"
