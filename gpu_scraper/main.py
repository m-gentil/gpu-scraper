import logging
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

from gpu_scraper.config import DEBUG, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from gpu_scraper.notifications.telegram import TelegramNotifier
from gpu_scraper.web.amd import Amd
from gpu_scraper.web.base import ProductProvider
from gpu_scraper.web.cast_informatica import CastInformatica

_LOGGER = logging.getLogger(__name__)

POLLING_INTERVAL_SECONDS = 2

ALL_PROVIDERS = [Amd(), CastInformatica()]


def poll_provider(provider: ProductProvider, notifier: TelegramNotifier) -> None:
    last_products = provider.get_available_products()

    _LOGGER.info(f"{provider.name} first has {last_products}")

    while True:
        time.sleep(POLLING_INTERVAL_SECONDS)
        curr_products = provider.retry_get_available_products()
        _LOGGER.info(f"{provider.name}: polled {len(curr_products)} available products")

        new_products = curr_products - last_products

        if new_products:
            _LOGGER.info(f"{provider.name} OLD: {last_products}")
            _LOGGER.info(f"{provider.name} NEW: {curr_products}")

        for product in new_products:
            _LOGGER.info(f"{provider.name}: NEW {product}")

            notifier.notify_product(product, provider.name)

        last_products = curr_products


def main() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s\t%(levelname)s:\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    _LOGGER.info("Starting...")
    notifier = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, debug_mode=DEBUG)

    with ThreadPoolExecutor() as tpe:
        [tpe.submit(poll_provider, provider, notifier) for provider in ALL_PROVIDERS]


if __name__ == "__main__":
    main()
