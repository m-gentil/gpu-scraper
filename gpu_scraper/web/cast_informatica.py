import logging

import requests

from gpu_scraper.constants import JSON_HEADERS, TIMEOUT_SECONDS
from gpu_scraper.product import Product
from gpu_scraper.web.base import ProductProvider

_LOGGER = logging.getLogger(__name__)


def _get_paginated_results(page_id: int) -> set[Product]:
    params = {"q": "Disponibilità-In magazzino", "page": str(page_id)}

    resp = requests.get(
        "https://castinformatica.it/1021-schede-video",
        params=params,
        headers=JSON_HEADERS,
        timeout=TIMEOUT_SECONDS,
    )
    resp.raise_for_status()

    parsed_resp = resp.json()

    return {
        Product(name=product["name"], link=product["url"], price=product["price_amount"])
        for product in parsed_resp["products"]
    }


class CastInformatica(ProductProvider):
    def get_available_products(self) -> set[Product]:
        curr_prods = _get_paginated_results(1)
        all_prods = curr_prods

        next_page = 2
        while curr_prods:
            curr_prods = _get_paginated_results(next_page)
            all_prods |= curr_prods

            next_page += 1

        return all_prods
