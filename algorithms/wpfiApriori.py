from typing import TypeVar, Generic
from models.item import Item
from models.transaction import Transaction
from utils.utils import Utils

E = TypeVar("E", bound="Item")
T = TypeVar("T", bound="Transaction")


class wPFIApriori(Generic[E, T]):
    def __init__(self, UD: list[T], items: set[E], m_sup: int, t: float, alpha: float):
        self.UD = UD
        self.items = items
        self.m_sup = m_sup
        self.t = t
        self.alpha = alpha

    def find_size_one_wPFI(self) -> list[set[E]]:
        sizeOneWpfis: list[set[E]] = []
        for i in self.items:
            itemList: set[E] = {i}

            if self.isWpfi(itemList):
                sizeOneWpfis.append(itemList)

        return sizeOneWpfis

    def isWpfi(self, item_set: set[E]) -> bool:
        support = Utils.get_support(self.UD, item_set)
        expected_support = Utils.get_expected_support(self.UD, item_set)
        avg_weight = Utils.get_avg_weight(item_set)
        lower_bound = max(
            Utils.get_lower_bound(expected_support, self.t, avg_weight), 0
        )
        upper_bound = min(
            Utils.get_upper_bound(expected_support, self.t, avg_weight), support
        )
        probabilistic_support = -1
        if self.m_sup >= lower_bound and self.m_sup <= upper_bound:
            probabilistic_vector = Utils.divide_and_conquer(self.UD, item_set)
            probabilistic_support = Utils.get_probabilistic_support(
                probabilistic_vector, self.t, avg_weight
            )

        return (lower_bound > self.m_sup) or (
            probabilistic_support >= self.m_sup and upper_bound >= self.m_sup
        )

    def wPFI_candidate_generate(self, W_PFIs: list[set[E]]):
        # initial list for result
        Ck: list[set[E]] = []
        # item set I' contains all distinct item in w_PFI list
        IPrime: set[E] = Utils.get_distinct_list_from_w_PFIs(W_PFIs)

        for X in W_PFIs:
            for item in Utils.get_difference_of_two_lists(IPrime, X):
                X_and_item = X.copy()
                X_and_item.add(item)

                if Utils.get_avg_weight(X_and_item) >= self.t:
                    if self.list_helper.not_existed_in_set(Ck, X_and_item):
                        Ck.append(X_and_item)

            minWeightItem = self.findMinWeightItem(
                X
            )  # find item has min weight in current item set X

            # loop in item set: I − I' − X (code line 10 in algorithm 2)
            for item in self.list_helper.get_different_of_two_list(
                self.list_helper.get_different_of_two_list(
                    self.all_distinct_item, IPrime
                ),
                X,
            ):
                # create temp item set X union current item
                X_and_item = X.copy()
                X_and_item.add(item)

                if self.calculator.get_avg_weight(
                    X_and_item
                ) >= self.t and item.getWeight() < (
                    0.0 if minWeightItem is None else minWeightItem.getWeight()
                ):
                    # list candidate doesn't contain that item set
                    if self.list_helper.not_existed_in_set(Ck, X_and_item):
                        Ck.append(X_and_item)  # add into candidate list

        return Ck
