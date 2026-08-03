"""
Infrastructure layer architecture tests.
"""

from pathlib import Path

from tests.architecture.helpers.imports import (
    get_imports,
    get_python_files,
)

INFRASTRUCTURE_PATH = Path("app/infrastructure")


FORBIDDEN_IMPORTS = (
    "app.api",
    "app.application",
)


def test_infrastructure_does_not_depend_on_upper_layers() -> None:
    """Infrastructure must not depend on API or application layers."""

    for file_path in get_python_files(INFRASTRUCTURE_PATH):
        imports = get_imports(file_path)

        for imported in imports:
            assert not imported.startswith(
                FORBIDDEN_IMPORTS,
            ), f"{file_path} imports forbidden module {imported}"
