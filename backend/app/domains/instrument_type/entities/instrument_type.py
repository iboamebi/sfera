"""
Domain entity: InstrumentType.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class InstrumentType(Entity):
    """Instrument type domain entity."""

    name: str
    manufacturer: str | None = None
    model: str | None = None
    measurement_type: str | None = None
    accuracy_class: str | None = None
    verification_interval_months: int | None = None
    description: str | None = None
    archived: bool = False

    def change_name(
        self,
        name: str,
    ) -> None:
        """Change instrument type name."""

        self.name = name

    def change_manufacturer(
        self,
        manufacturer: str | None,
    ) -> None:
        """Change instrument type manufacturer."""

        self.manufacturer = manufacturer

    def change_model(
        self,
        model: str | None,
    ) -> None:
        """Change instrument type model."""

        self.model = model

    def change_measurement_type(
        self,
        measurement_type: str | None,
    ) -> None:
        """Change instrument type measurement type."""

        self.measurement_type = measurement_type

    def change_accuracy_class(
        self,
        accuracy_class: str | None,
    ) -> None:
        """Change instrument type accuracy class."""

        self.accuracy_class = accuracy_class

    def change_verification_interval_months(
        self,
        verification_interval_months: int | None,
    ) -> None:
        """Change instrument type verification interval."""

        self.verification_interval_months = verification_interval_months

    def change_description(
        self,
        description: str | None,
    ) -> None:
        """Change instrument type description."""

        self.description = description

    def archive(
        self,
    ) -> None:
        """Archive instrument type."""

        self.archived = True

    def restore(
        self,
    ) -> None:
        """Restore instrument type."""

        self.archived = False
