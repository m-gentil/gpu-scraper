from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    name: str
    link: str
    price: Optional[float] = None
