from app.shared.events.event_dispatcher import EventDispatcher
from app.domains.device.events.device_connected import DeviceConnected


def test_event_dispatcher():

    result = []

    dispatcher = EventDispatcher()

    dispatcher.register(
        DeviceConnected,
        lambda event: result.append(
            event.device_id
        ),
    )

    event = DeviceConnected(
        device_id="123"
    )

    dispatcher.dispatch(event)

    assert result == ["123"]
