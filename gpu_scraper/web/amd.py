import logging

import requests
from bs4 import BeautifulSoup

from gpu_scraper.constants import DEFAULT_HEADERS, TIMEOUT_SECONDS
from gpu_scraper.product import Product
from gpu_scraper.web.base import ProductProvider

_LOGGER = logging.getLogger(__name__)


class Amd(ProductProvider):
    name = "AMD"

    def get_available_products(self) -> set[Product]:
        resp = requests.get(
            "https://www.amd.com/en/direct-buy/it", headers=DEFAULT_HEADERS, timeout=TIMEOUT_SECONDS
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        products_on_sale = soup.find_all("div", class_="direct-buy")

        if len(products_on_sale) == 0:
            _LOGGER.warning("AMD: No products on sale")
            raise ValueError("AMD: No products on sale")

        products: set[Product] = set()
        for element in products_on_sale:
            button = element.find("button")
            if not button:  # The product is unavailable
                continue

            product_id = button["href"].split("/")[-1]

            link = f"https://www.amd.com/en/direct-buy/{product_id}"
            name = button.find("span").text
            price = float(
                element.find("div", class_="shop-price")
                .text.replace("€", "")
                .replace(",", ".")
                .strip()
            )
            products.add(Product(name, link, price))

        return products


if __name__ == "__main__":
    print(Amd().get_available_products())
