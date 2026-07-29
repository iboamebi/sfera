# backend/app/domain/repositories/price_list_repository.py
# PriceList repository interface

from abc import ABC, abstractmethod
from uuid import UUID


class PriceListRepository(ABC):
    """
    Domain repository interface for PriceList entity.
    """

    @abstractmethod
    def get(self, price_list_id: UUID):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def update(self, price_list, data):
        raise NotImplementedError
