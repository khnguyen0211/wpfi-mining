from typing import TypeVar, Generic, Set, List

import numpy as np
import math
from scipy.stats import poisson

from models.item import Item
from models.transaction import Transaction

E = TypeVar("E", bound="Item")
T = TypeVar("T", bound="Transaction")


class Utils(Generic[E, T]):

    @staticmethod
    def format_double(number: float, decimal_places=2) -> float:
        return round(number, decimal_places)

    @staticmethod
    def is_list_contained(larger: List[E], small: Set[E]) -> bool:
        return set(larger).issuperset(small)

    @staticmethod
    def not_existed_in_set(Ck: List[Set[E]], candidate: Set[E]) -> bool:
        for set_item in Ck:
            if set_item.issuperset(candidate) and len(set_item) == len(candidate):
                return False
        return True

    @staticmethod
    def get_difference_of_two_lists(first_list: Set[E], second_list: Set[E]) -> set[E]:
        difference_set = set(first_list)
        difference_set.difference_update(second_list)
        return difference_set

    @staticmethod
    def get_distinct_list_from_w_PFIs(W_PFIs: list[set[E]]) -> set[E]:
        set_item = set()
        for item_list in W_PFIs:
            set_item.update(item_list)
        return set_item

    @staticmethod
    def divide(from_index: int, to_index: int, UD: list[T]):
        return UD[from_index : to_index + 1]

    @staticmethod
    def convolution(fx1, fx2, k):
        rs = 0.0
        for i in range(k + 1):
            if i < len(fx1) and (k - i) < len(fx2):
                rs += fx1[i] * fx2[k - i]
        return rs

    @staticmethod
    def dynamic_programming(UD: list[T], item_set: set[E]):
        n = len(UD)
        fx = np.zeros(n + 1)
        fx[0] = 1
        for i in range(n):
            t = UD[i]
            pix = (
                t.get_probability_of_item_set(item_set)
                if Utils.is_list_contained(list(t.get_items().keys()), item_set)
                else 0.0
            )
            fPrimeX = np.zeros(n + 1)
            fPrimeX[0] = (1 - pix) * fx[0]
            for k in range(1, n + 1):
                fPrimeX[k] = pix * fx[k - 1] + (1 - pix) * fx[k]
            fx = fPrimeX.copy()
        return fx

    @staticmethod
    def divide_and_conquer(UD: list[T], item_set: set[E]):
        n = len(UD)
        fx = np.zeros(n + 1)
        if n == 1:
            Ti = UD[0]
            pix = (
                Ti.get_probability_of_item_set(item_set)
                if Utils.is_list_contained(list(Ti.get_items().keys()), item_set)
                else 0.0
            )
            fx[0] = 1 - pix
            fx[1] = pix
            return fx
        DB1 = Utils.divide(0, (n // 2) - 1, UD)
        DB2 = Utils.divide(n // 2, n - 1, UD)
        fx_1 = Utils.divide_and_conquer(DB1, item_set)
        fx_2 = Utils.divide_and_conquer(DB2, item_set)
        for k in range(n + 1):
            fx[k] = Utils.convolution(fx_1, fx_2, k)
        return fx

    @staticmethod
    def get_support(UD: list[T], item_set: set[E]) -> int:
        support = 0
        for trans in UD:
            item = set(trans.get_items().keys())
            if item.issuperset(item_set):
                support += 1
        return support

    @staticmethod
    def get_expected_support(UD: list[T], item_set: set[E]):
        rs = 0.0
        for trans in UD:
            if set(trans.get_items().keys()).issuperset(item_set):
                rs += trans.get_probability_of_item_set(item_set)
        return Utils.format_double(rs)

    @staticmethod
    def get_avg_weight(item_set: set[E]):
        sum_weight = sum(item.get_weight() for item in item_set)
        return Utils.format_double(sum_weight / len(item_set))

    @staticmethod
    def get_probabilistic_support(
        probabilistic_vector: list[float], t: float, weight: float
    ) -> int:
        total_probability = 0.0
        for i in range(len(probabilistic_vector) - 1, -1, -1):
            total_probability += probabilistic_vector[i]
            if float(Utils.format_double(total_probability * weight)) >= t:
                return i
        return 0

    @staticmethod
    def get_upper_bound(expected_support: float, t: float, weight: float):
        a = t / max(weight, 1e-10)
        x = math.log(a) ** 2 - 8 * expected_support * math.log(max(a, 1e-10))
        y = 0.5 * (
            2 * expected_support - math.log(max(a, 1e-10)) + math.sqrt(math.fabs(x))
        )
        return Utils.format_double(y)

    @staticmethod
    def get_lower_bound(expected_support: float, t: float, weight: float):
        a = t / max(weight, 1e-10)
        y = expected_support - math.sqrt(
            math.fabs(-2 * expected_support * math.log(max(math.fabs(1 - a), 1e-10)))
        )
        return Utils.format_double(y)

    @staticmethod
    def find_min_weight_item(item_set: set[E]) -> E | None:
        if not item_set:
            return None

        min_weight = min(item.get_weight() for item in item_set)

        for item in item_set:
            if item.get_weight() == min_weight:
                return item

        return None

    @staticmethod
    def f_poisson(x: float, u: float, t: float, m: float) -> float:
        a = poisson(u)
        return a.cdf(math.floor(x)) + (t / m) - 1

    @staticmethod
    def derivative_f_poisson(x: float, u: float) -> float:
        a = poisson(u)
        total = 0.0
        for k in range(math.floor(abs(x)) + 1):
            total += a.pmf(k) * (k / u - 1)
        return total

    @staticmethod
    def newton_raphson_method(x: float, u: float, t: float, m: float) -> float:
        EPSILON = 1e-10
        while True:
            derivative = Utils.derivative_f_poisson(x, u)
            if abs(derivative) < EPSILON:
                break
            h = Utils.f_poisson(x, u, t, m) / derivative
            if abs(h) < EPSILON:
                break
            u = u - h
        return u

    def probabilistic_condition(
        UD: list[T], m_sup: float, t: float, alpha: float, item_set: Set[E], item: E
    ) -> bool:
        muy_x = Utils.get_expected_support(UD, item_set)

        muy_y = Utils.get_expected_support(UD, {item})

        n = len(UD)

        max_weight = max(Utils.get_avg_weight(item_set), item.get_weight())

        muy_hat = Utils.newton_method(m_sup - 1, m_sup, t, max_weight)

        return min(muy_x, muy_y) >= muy_hat and muy_x * muy_y >= alpha * n * muy_hat
