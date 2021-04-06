from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class Product:
    name: str
    link: str
    price: Optional[float] = None

    def __hash__(self) -> int:
        return hash(self.name + self.link)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Product) and self.name == other.name and self.link == other.link
