import logging
from dataclasses import dataclass

import requests
from tenacity import retry, wait_exponential

from gpu_scraper.product import Product

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class TelegramNotifier:
    token: str
    chat_id: str

    debug_mode: bool = False

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10))  # type: ignore
    def _send_message(self, message: str) -> None:
        _LOGGER.info(f"Notifier: sending {message}")
        if self.debug_mode:
            return

        params = {"chat_id": self.chat_id, "parse_mode": "Markdown", "text": message}

        resp = requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage", params=params)
        resp.raise_for_status()

    def notify_product(self, product: Product, provider_name: str) -> None:
        price_str = f" for € {product.price}" if product.price else ""
        self._send_message(
            f"{provider_name} has {product.name} at [link]({product.link}){price_str}"
        )
