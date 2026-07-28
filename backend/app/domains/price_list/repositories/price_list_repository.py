from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.price_list.entities.price_list import PriceList


class PriceListRepository(ABC):
    """
    Интерфейс репозитория прайс-листов.
    """

    @abstractmethod
    async def get_by_id(
        self,
        price_list_id: UUID,
    ) -> PriceList | None:
        """
        Получение прайс-листа по идентификатору.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_active(
        self,
    ) -> PriceList | None:
        """
        Получение активного прайс-листа.
        """

        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
    ) -> list[PriceList]:
        """
        Получение списка прайс-листов.
        """

        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        price_list: PriceList,
    ) -> PriceList:
        """
        Сохранение прайс-листа.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        price_list_id: UUID,
    ) -> None:
        """
        Удаление прайс-листа.
        """

        raise NotImplementedError
