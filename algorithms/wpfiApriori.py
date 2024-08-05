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

    def wpfi_apriori_mining(self):
        w_PFI_final = []
        w_PFI_1 = self.find_size_one_wpfi()
        w_PFI_final.append(w_PFI_1)
        k = 1
        while w_PFI_final[k - 1]:
            Ck = self.generate_wpfi_candidates_optimize(w_PFI_final[k - 1])
            w_PFI_k = self.find_size_k_wpfi(Ck)
            w_PFI_final.append(w_PFI_k)
            k += 1

        w_PFI_final = [x for x in w_PFI_final if x]

        return w_PFI_final

    def find_size_one_wpfi(self) -> list[set[E]]:
        sizeOneWpfis: list[set[E]] = []
        for i in self.items:
            itemList: set[E] = {i}

            if self.is_wpfi(itemList):
                sizeOneWpfis.append(itemList)

        return sizeOneWpfis

    def is_wpfi(self, item_set: set[E]) -> bool:
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

    def generate_wpfi_candidates(self, W_PFIs: list[set[E]]):
        Ck: list[set[E]] = []
        IPrime: set[E] = Utils.get_distinct_list_from_w_PFIs(W_PFIs)

        for X in W_PFIs:
            difference_of_two_lists: set[E] = Utils.get_difference_of_two_lists(
                IPrime, X
            )

            for item in difference_of_two_lists:
                X_and_item = X.copy()
                X_and_item.add(item)

                if Utils.get_avg_weight(X_and_item) >= self.t:
                    if Utils.not_existed_in_set(Ck, X_and_item):
                        Ck.append(X_and_item)

            minWeightItem: E = Utils.find_min_weight_item(X)
            difference_of_two_nested_lists: set[E] = Utils.get_difference_of_two_lists(
                Utils.get_difference_of_two_lists(self.items, IPrime),
                X,
            )

            for item in difference_of_two_nested_lists:
                X_and_item = X.copy()
                X_and_item.add(item)

                if Utils.get_avg_weight(X_and_item) >= self.t and item.get_weight() < (
                    0.0 if minWeightItem is None else minWeightItem.get_weight()
                ):
                    if Utils.not_existed_in_set(Ck, X_and_item):
                        Ck.append(X_and_item)

        return Ck

    def generate_wpfi_candidates_optimize(self, W_PFIs: list[set[E]]):
        Ck: list[set[E]] = []
        IPrime: set[E] = Utils.get_distinct_list_from_w_PFIs(W_PFIs)

        for X in W_PFIs:
            difference_of_two_lists: set[E] = Utils.get_difference_of_two_lists(
                IPrime, X
            )

            for item in difference_of_two_lists:
                X_and_item = X.copy()
                X_and_item.add(item)

                if Utils.get_avg_weight(X_and_item) >= self.t:
                    if Utils.probabilistic_condition(
                        self.UD, self.m_sup, self.t, self.alpha, X, item
                    ):
                        if Utils.not_existed_in_set(Ck, X_and_item):
                            Ck.append(X_and_item)

            minWeightItem: E = Utils.find_min_weight_item(X)
            difference_of_two_nested_lists: set[E] = Utils.get_difference_of_two_lists(
                Utils.get_difference_of_two_lists(self.items, IPrime),
                X,
            )

            for item in difference_of_two_nested_lists:
                X_and_item = X.copy()
                X_and_item.add(item)

                if Utils.get_avg_weight(X_and_item) >= self.t and item.get_weight() < (
                    0.0 if minWeightItem is None else minWeightItem.get_weight()
                ):
                    if Utils.probabilistic_condition(
                        self.UD, self.m_sup, self.t, self.alpha, X, item
                    ):
                        if Utils.not_existed_in_set(Ck, X_and_item):
                            Ck.append(X_and_item)

        return Ck

    def find_size_k_wpfi(self, candidates: list[set[E]]):
        return [candidate for candidate in candidates if self.is_wpfi(candidate)]
