# PriceList application service.
# Coordinates PriceList use cases between API layer and domain layer.

from uuid import UUID

from app.application.price_list.commands.activate_price_list import (
    ActivatePriceListCommand,
)
from app.application.price_list.commands.add_price_list_item import (
    AddPriceListItemCommand,
)
from app.application.price_list.commands.create_price_list import (
    CreatePriceListCommand,
)
from app.application.price_list.commands.remove_price_list_item import (
    RemovePriceListItemCommand,
)
from app.application.price_list.commands.update_price_list import (
    UpdatePriceListCommand,
)
from app.application.price_list.commands.update_price_list_item import (
    UpdatePriceListItemCommand,
)
from app.application.price_list.exceptions import (
    PriceListNotFoundApplicationError,
)
from app.domains.price_list.entities.price_list import PriceList
from app.domains.price_list.entities.price_list_item import PriceListItem
from app.domains.price_list.repositories.price_list_repository import (
    PriceListRepository,
)


class PriceListApplicationService:
    """
    Application service for PriceList business scenarios.
    """

    def __init__(
        self,
        repository: PriceListRepository,
    ):
        self.repository = repository

    async def get_price_list(
        self,
        price_list_id: UUID,
    ) -> PriceList | None:
        """
        Returns PriceList by identifier.
        """

        return await self.repository.get_by_id(price_list_id)

    async def get_active_price_list(
        self,
    ) -> PriceList | None:
        """
        Returns active PriceList.
        """

        return await self.repository.get_active()

    async def list_price_lists(
        self,
    ) -> list[PriceList]:
        """
        Returns all PriceLists.
        """

        return await self.repository.list()

    async def create(
        self,
        command: CreatePriceListCommand,
    ) -> PriceList:
        """
        Creates new PriceList.
        """

        price_list = PriceList(
            name=command.name,
            description=command.description,
        )

        return await self.repository.save(price_list)

    async def update(
        self,
        command: UpdatePriceListCommand,
    ) -> PriceList:
        """
        Updates existing PriceList.
        """

        price_list = await self.repository.get_by_id(command.price_list_id)

        if price_list is None:
            raise PriceListNotFoundApplicationError

        price_list.change_name(
            command.name,
        )

        price_list.change_description(
            command.description,
        )

        return await self.repository.save(price_list)

    async def activate(
        self,
        command: ActivatePriceListCommand,
    ) -> PriceList:
        """
        Activates PriceList.
        """

        price_list = await self.repository.get_by_id(command.price_list_id)

        if price_list is None:
            raise PriceListNotFoundApplicationError

        price_list.activate()

        return await self.repository.save(price_list)

    async def add_item(
        self,
        command: AddPriceListItemCommand,
    ) -> PriceList:
        """
        Adds item to PriceList.
        """

        price_list = await self.repository.get_by_id(command.price_list_id)

        if price_list is None:
            raise PriceListNotFoundApplicationError

        item = PriceListItem(
            service_code=command.service_code,
            name=command.name,
            price=command.price,
            unit=command.unit,
            description=command.description,
        )

        price_list.add_item(item)

        return await self.repository.save(price_list)

    async def remove_item(
        self,
        command: RemovePriceListItemCommand,
    ) -> PriceList:
        """
        Removes item from PriceList.
        """

        price_list = await self.repository.get_by_id(command.price_list_id)

        if price_list is None:
            raise PriceListNotFoundApplicationError

        price_list.remove_item(command.item_id)

        return await self.repository.save(price_list)

    async def update_item(
        self,
        command: UpdatePriceListItemCommand,
    ) -> PriceList:
        """
        Updates item in PriceList.
        """

        price_list = await self.repository.get_by_id(command.price_list_id)

        if price_list is None:
            raise PriceListNotFoundApplicationError

        if command.price is not None:
            price_list.change_item_price(
                command.item_id,
                command.price,
            )

        if command.description is not None:
            price_list.change_item_description(
                command.item_id,
                command.description,
            )

        return await self.repository.save(price_list)
