from typing import TypeVar, Generic, Dict, Set
from models.item import Item

E = TypeVar("E", bound="Item")


class Transaction(Generic[E]):
    def __init__(self, items: Dict[E, float] = None):
        if items is None:
            self.items = {}
        else:
            self.items = items

    def get_probability_of_item_set(self, item_set_X: Set[E]) -> float:
        rs = 1.0
        for item in item_set_X:
            if item in self.items:
                rs *= self.items[item]
        return rs

    def get_items(self) -> Dict[E, float]:
        return self.items

    def __str__(self) -> str:
        s = []
        for item, probability in self.items.items():
            s.append(f"({item.get_name()}, {probability})")
        return ", ".join(s)
