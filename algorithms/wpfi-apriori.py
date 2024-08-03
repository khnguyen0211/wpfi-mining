from typing import TypeVar, Generic, List, Set
from models.item import Item
from models.transaction import Transaction

E = TypeVar('E', bound='Item')
T = TypeVar('T', bound='Transaction')

class wPFI_Apriori(Generic[E, T]):
    def __init__(self, UD: List[T], all_distinct_item: Set[E], m_sup: int, t: float, alpha: float):
        self.UD = UD
        self.all_distinct_item = all_distinct_item
        self.m_sup = m_sup
        self.t = t
        self.alpha = alpha
    
    def helloApriori():
        return 'Hello Apriori'