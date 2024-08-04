import random
from typing import TypeVar, Generic, List, Set, Dict

from models.item import Item
from models.transaction import Transaction

E = TypeVar("E", bound="Item")
T = TypeVar("T", bound="Transaction")


class Dataset(Generic[E, T]):
    def __init__(self, file_path: str, num: int):
        self.UD: List[T] = []
        self.items: Set[E] = set()
        self.read_file(file_path, num)

    def read_file(self, file_path: str, num: int):
        count_line = 0
        with open(file_path, "r") as file:
            for line in file:
                if count_line == num:
                    break
                count_line += 1
                item_set = line.strip().split()
                trans = Transaction()
                for item_string in item_set:
                    if self.not_contained(item_string):
                        item = Item(item_string, self.uniform_distribution())
                        self.items.add(item)
                    else:
                        item = self.find_item_by_name(item_string)
                    trans.get_items()[item] = self.gaussian_distribution(0.5, 0.125)
                self.UD.append(trans)

    @staticmethod
    def write_file(path: str, rows: List) -> bool:
        try:
            with open(path, "w") as writer:
                for row in rows:
                    writer.write(str(row) + "\n")
            return True
        except IOError:
            print("Error.")
            return False
        except Exception:
            print("Cannot write file")
            return False

    def get_dataset(self) -> List[T]:
        return self.UD

    def get_items(self) -> Set[E]:
        return self.items

    @staticmethod
    def gaussian_distribution(mean: float, variance: float) -> float:
        while True:
            gaussian = random.gauss(mean, variance**0.5)
            if 0 < gaussian < 1:
                return gaussian

    @staticmethod
    def uniform_distribution() -> float:
        return random.random()

    def not_contained(self, item_name: str) -> bool:
        return not any(i.name.lower() == item_name.lower() for i in self.items)

    def find_item_by_name(self, item_name: str) -> E:
        for i in self.items:
            if i.name.lower() == item_name.lower():
                return i
        return None
