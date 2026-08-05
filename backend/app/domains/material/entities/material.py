"""
Domain entity: Material.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Material(Entity):
    """Material entity."""

    name: str
    article: str | None = None
    unit: str = ""
    description: str | None = None
    archived: bool = False

    def change_name(
        self,
        name: str,
    ) -> None:
        """Change material name."""

        self.name = name

    def change_article(
        self,
        article: str | None,
    ) -> None:
        """Change material article."""

        self.article = article

    def change_unit(
        self,
        unit: str,
    ) -> None:
        """Change material unit."""

        self.unit = unit

    def change_description(
        self,
        description: str | None,
    ) -> None:
        """Change material description."""

        self.description = description

    def archive(
        self,
    ) -> None:
        """Archive material."""

        self.archived = True

    def restore(
        self,
    ) -> None:
        """Restore archived material."""

        self.archived = False
