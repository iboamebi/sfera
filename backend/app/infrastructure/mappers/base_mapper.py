"""
Base mapper interface.
"""

from abc import ABC, abstractmethod
from typing import TypeVar

DomainT = TypeVar("DomainT")
OrmT = TypeVar("OrmT")


class BaseMapper[DomainT, OrmT](ABC):
    """Base mapper."""

    @abstractmethod
    def to_domain(
        self,
        model: OrmT,
    ) -> DomainT: ...

    @abstractmethod
    def to_model(
        self,
        entity: DomainT,
        model: OrmT,
    ) -> OrmT: ...
