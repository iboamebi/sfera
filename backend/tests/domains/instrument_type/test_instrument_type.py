"""
Domain tests: InstrumentType.
"""

from uuid import uuid4

from app.domains.instrument_type.entities.instrument_type import InstrumentType


def test_instrument_type_lifecycle():
    instrument_type = InstrumentType(
        id=uuid4(),
        name="Pressure gauge",
    )

    instrument_type.change_name("Digital pressure gauge")
    instrument_type.change_manufacturer("ACME")
    instrument_type.change_model("PG-100")
    instrument_type.change_measurement_type("Pressure")
    instrument_type.change_accuracy_class("0.5")
    instrument_type.change_verification_interval_months(12)
    instrument_type.change_description("Test instrument type")

    assert instrument_type.name == "Digital pressure gauge"
    assert instrument_type.manufacturer == "ACME"
    assert instrument_type.model == "PG-100"
    assert instrument_type.measurement_type == "Pressure"
    assert instrument_type.accuracy_class == "0.5"
    assert instrument_type.verification_interval_months == 12
    assert instrument_type.description == "Test instrument type"
    assert instrument_type.archived is False

    instrument_type.archive()

    assert instrument_type.archived is True

    instrument_type.restore()

    assert instrument_type.archived is False
