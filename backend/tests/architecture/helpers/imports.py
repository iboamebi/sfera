"""
Import analysis helpers for architecture tests.
"""

import ast
from pathlib import Path


def get_python_files(
    path: Path,
) -> list[Path]:
    """Return Python files recursively."""

    return list(path.rglob("*.py"))


def get_imports(
    file_path: Path,
) -> list[str]:
    """Extract imported module names from Python file."""

    tree = ast.parse(
        file_path.read_text(
            encoding="utf-8",
        ),
    )

    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(
                node.module,
            )

    return imports
