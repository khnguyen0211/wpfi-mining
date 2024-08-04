from typing import TypeVar, Generic
from models.item import Item

E = TypeVar("E", bound="Item")


class Transaction(Generic[E]):
    def __init__(self, items: dict[E, float] = None):
        if items is None:
            self.items = {}
        else:
            self.items = items

    def get_probability_of_item_set(self, item_set_X: set[E]) -> float:
        rs = 1.0
        for item in item_set_X:
            if item in self.items:
                rs *= self.items[item]
        return rs

    def get_items(self) -> dict[E, float]:
        return self.items

    def __str__(self) -> str:
        s = []
        for item, probability in self.items.items():
            s.append(f"({item.get_name()}, {probability})")
        return ", ".join(s)

    def __repr__(self):
        return self.__str__()
