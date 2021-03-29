import logging
from abc import ABC, abstractmethod

from tenacity import after_log, retry, wait_exponential

from gpu_scraper.product import Product

_LOGGER = logging.getLogger(__name__)


class ProductProvider(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_available_products(self) -> set[Product]:
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=10),  # type: ignore
        after=after_log(_LOGGER, logging.WARNING),  # type: ignore
    )
    def retry_get_available_products(self) -> set[Product]:
        return self.get_available_products()
