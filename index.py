from models.item import Item
from models.transaction import Transaction
from models.node import Node

milk = Item("Milk", 0.4)
fruit = Item("Fruit", 0.9)
video = Item("Video", 0.6)

tom_transaction = Transaction({milk: 0.4, fruit: 1.0, video: 0.3})
lucy_transaction = Transaction({milk: 1.0, fruit: 0.8})

print(video)

item_set = {milk, fruit, video}

node = Node(
    item_set=item_set,
    sup=2.0,
    e_sup=1.5,
    p_sup=0.8,
    lb=0.3,
    ub=0.9,
    parent=None,
    children=[],
    avg_weight=0.75
)




