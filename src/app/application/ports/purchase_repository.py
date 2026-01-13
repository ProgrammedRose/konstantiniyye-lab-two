
from abc import ABC, abstractmethod
from typing import List
from src.app.domain.entities.purchase import Purchase


class PurchaseRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Purchase]:
        pass

    @abstractmethod
    def add(self, purchase: Purchase) -> None:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
