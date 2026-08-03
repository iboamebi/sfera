"""
Domain layer architecture tests.
"""

from pathlib import Path

from tests.architecture.helpers.imports import (
    get_imports,
    get_python_files,
)

DOMAIN_PATH = Path("app/domains")


FORBIDDEN_IMPORTS = (
    "app.api",
    "app.infrastructure",
    "app.models",
    "sqlalchemy",
)


def test_domain_does_not_depend_on_outer_layers() -> None:
    """Domain must not depend on infrastructure or API layers."""

    for file_path in get_python_files(DOMAIN_PATH):
        imports = get_imports(file_path)

        for imported in imports:
            assert not imported.startswith(
                FORBIDDEN_IMPORTS,
            ), f"{file_path} imports forbidden module {imported}"
