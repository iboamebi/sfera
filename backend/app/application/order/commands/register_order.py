from dataclasses import dataclass

from app.domains.order.entities.order import Order


@dataclass(frozen=True)
class RegisterOrderCommand:
    order: Order


class RegisterOrderHandler:

    def handle(
        self,
        command: RegisterOrderCommand,
    ) -> Order:

        command.order.register()

        return command.order
