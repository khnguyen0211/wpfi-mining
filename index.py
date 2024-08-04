from models.item import Item
from models.transaction import Transaction
from models.node import Node
from utils.utils import Utils

milk = Item("Milk", 0.4)
fruit = Item("Fruit", 0.9)
video = Item("Video", 0.6)


def list_helper():
    # 1. Test is_list_contained -> Passed
    larger = [milk, fruit, video]
    smaller = [fruit]
    print("#1", Utils.is_list_contained(larger, smaller))

    # 2. Test not_existed_in_set -> Passed
    ck = [{milk, fruit}, {fruit, video}, {fruit, milk}]
    candies = {video, milk}
    print("#2", Utils.not_existed_in_set(ck, candies))

    # 3. Test get_difference_of_two_lists -> Passed
    subSet = Utils.get_difference_of_two_lists(larger, smaller)
    print("#3", ", ".join(map(str, subSet)))

    # 4. Test get_distinct_list_from_w_PFIs -> Passed
    wPFIs = [{milk, fruit, video}, {fruit, video}, {fruit, milk}]
    subSet = Utils.get_distinct_list_from_w_PFIs(wPFIs)
    print("#4", ", ".join(map(str, subSet)))


tom_transaction = Transaction({milk: 0.4, fruit: 1.0, video: 0.3})
lucy_transaction = Transaction({milk: 1.0, fruit: 0.8})
jerry_transaction = Transaction({milk: 0.6, video: 0.2})

item_set: set[Item] = {milk, fruit, video}
US: list[Transaction] = [tom_transaction, lucy_transaction, jerry_transaction]


def calculator():
    # Test get_support -> Passed
    item_set: set[Item] = {milk}
    result = Utils.get_support(US, item_set)
    print("#5", result)

    # Test get_expected_support -> Passed
    item_set: set[Item] = {milk}
    result = Utils.get_expected_support(US, item_set)
    print("#6", result)

    # Test get_avg_weight -> Passed
    item_set: set[Item] = {milk, fruit, video}
    result = Utils().get_avg_weight({milk, fruit, video})
    print("#7", result)

    # Test get_lower_bound -> Passed
    floats = [2, 2.5, 3]
    print("#8", Utils.get_lower_bound(floats[0], floats[1], floats[2]))

    # Test get_upper_bound -> Passed
    print("#9", Utils.get_upper_bound(floats[0], floats[1], floats[2]))

    # Test get_probabilistic_support -> Passed
    floats = [0.1, 0.15, 0.2, 0.15, 0.12, 0.18, 0.06, 0.04]
    mp = 0.3
    w = 0.5
    result = Utils().get_probabilistic_support(floats, mp, w)
    print("#10", result)

    # Test dynamic_programming ->
    print("#11", Utils().divide_and_conquer(US, item_set))


calculator()

list_helper()
