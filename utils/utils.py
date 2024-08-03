from typing import TypeVar, Generic, Set, List

from models.item import Item
from models.transaction import Transaction

E = TypeVar('E', bound='Item')
T = TypeVar('T', bound='Transaction')

def formatDouble(number, decimal_places=2) -> float:
    return round(number, decimal_places)

def is_list_contained(self, larger: List[E], small: Set[E]) -> bool:
    return set(larger).issuperset(small)

def not_existed_in_set(self, Ck: List[Set[E]], candidate: Set[E]) -> bool:
    for set_item in Ck:
        if set_item.issuperset(candidate) and len(set_item) == len(candidate):
            return False
    return True

def get_difference_of_two_lists(self, first_list: Set[E], second_list: Set[E]) -> Set[E]:
    difference_set = set(first_list)
    difference_set.difference_update(second_list)
    return difference_set

def get_distinct_list_from_w_PFIs(self, W_PFIs: List[Set[E]]) -> Set[E]:
    set_item = set()
    for item_list in W_PFIs:
        set_item.update(item_list)
    return set_item