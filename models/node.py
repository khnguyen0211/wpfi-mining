from typing import TypeVar, Generic, Set, List
from models.item import Item
from models.transaction import Transaction
from utils.utils import formatDouble

E = TypeVar('E', bound='Item')
T = TypeVar('T', bound='Transaction')

class Node(Generic[E, T]):
    def __init__(self, item_set: Set[E] = None, sup: float = 0.0, e_sup: float = 0.0, p_sup: float = 0.0,
                 lb: float = 0.0, ub: float = 0.0, parent: 'Node[E, T]' = None,
                 children: List['Node[E, T]'] = None, avg_weight: float = 0.0):
        self.item_set = item_set or set()
        self.sup = sup
        self.e_sup = e_sup
        self.p_sup = p_sup
        self.lb = lb
        self.ub = ub
        self.parent = parent
        self.children = children or []
        self.avg_weight = avg_weight
        self.iswPFI = False

    def get_parent(self) -> 'Node[E, T]':
        return self.parent

    def set_parent(self, parent: 'Node'):
        self.parent = parent

    def get_item_set(self) -> Set[E]:
        return self.item_set

    def set_item_set(self, item_set: Set[E]):
        self.item_set = item_set

    def set_sup(self, sup: float):
        self.sup = sup

    def get_e_sup(self) -> float:
        return self.e_sup

    def set_e_sup(self, e_sup: float):
        self.e_sup = e_sup

    def get_p_sup(self) -> float:
        return self.p_sup

    def set_p_sup(self, p_sup: float):
        self.p_sup = p_sup

    def set_lb(self, lb: float):
        self.lb = lb

    def set_ub(self, ub: float):
        self.ub = ub

    def get_children(self) -> List['Node[E, T]']:
        return self.children

    def set_children(self, children: List['Node[E, T]']):
        self.children = children

    def check_wPFI(self, m_sup: int) -> bool:
        if self.lb > m_sup:
            return True
        if self.ub < m_sup:
            return False
        return self.p_sup >= m_sup

    def __str__(self) -> str:
        s = "[" + ", ".join(str(i) for i in self.item_set) + "]"
        y = "["
        if self.parent is not None:
            if self.parent.get_item_set():
                y += ", ".join(str(i) for i in self.parent.get_item_set())
            else:
                y += "Root"
        y += "]"
        return (f"{s}, {formatDouble(self.sup)}, {formatDouble(self.e_sup)}, "
                f"{'?' if self.p_sup == -1 else formatDouble(self.p_sup)}, "
                f"{formatDouble(self.lb)}, {formatDouble(self.ub)}, {y}, "
                f"{formatDouble(self.avg_weight)} => {self.iswPFI}")

    def get_node_name(self) -> str:
        return "[" + ", ".join(str(i) for i in self.item_set) + "]"

    def get_avg_weight(self) -> float:
        return self.avg_weight

    def is_wPFI(self) -> bool:
        return self.iswPFI

    def set_iswPFI(self, iswPFI: bool):
        self.iswPFI = iswPFI