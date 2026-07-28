# backend/app/application/services/price_list_service.py
# Application service for PriceList operations

from uuid import UUID


class PriceListService:
    """
    Application layer service for PriceList use cases.
    """

    def __init__(self, repository):
        self.repository = repository

    def get_price_list(self, price_list_id: UUID):
        return self.repository.get(price_list_id)

    def get_price_lists(self):
        return self.repository.get_all()

    def create_price_list(self, data):
        return self.repository.create(data)

    def update_price_list(self, price_list_id: UUID, data):
        price_list = self.repository.get(price_list_id)

        if price_list is None:
            return None

        return self.repository.update(
            price_list,
            data,
        )
