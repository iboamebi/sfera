"""
Domain exceptions for PriceList context.
"""


class PriceListDomainError(Exception):
    """
    Базовое исключение домена PriceList.
    """

    pass


class InvalidPriceListNameError(PriceListDomainError):
    """
    Ошибка пустого или некорректного названия прайс-листа.
    """

    def __init__(self):
        super().__init__("Price list name cannot be empty")


class PriceListAlreadyActiveError(PriceListDomainError):
    """
    Попытка повторной активации активного прайс-листа.
    """

    def __init__(self):
        super().__init__("Price list is already active")


class PriceListNotActiveError(PriceListDomainError):
    """
    Операция требует активный прайс-лист.
    """

    def __init__(self):
        super().__init__("Price list is not active")


class PriceListItemAlreadyExistsError(PriceListDomainError):
    """
    Попытка добавить дубликат позиции.
    """

    def __init__(
        self,
        service_code: str,
    ):
        super().__init__(f"Price list item already exists: {service_code}")


class InvalidPriceError(PriceListDomainError):
    """
    Некорректное значение цены.
    """

    def __init__(
        self,
        price: object,
    ):
        super().__init__(f"Invalid price value: {price}")


class PriceListItemNotFoundError(PriceListDomainError):
    """
    Позиция прайс-листа не найдена.
    """

    def __init__(
        self,
        item_id: object,
    ):
        super().__init__(f"Price list item not found: {item_id}")
