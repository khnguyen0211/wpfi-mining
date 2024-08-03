from models.item import Item
from models.transaction import Transaction
from models.node import Node
from typing import  Set

milk = Item("Milk", 0.4)
fruit = Item("Fruit", 0.9)
video = Item("Video", 0.6)

tom_transaction = Transaction({milk: 0.4, fruit: 1.0, video: 0.3})
lucy_transaction = Transaction({milk: 1.0, fruit: 0.8})
item_set: Set[Item] = {milk, fruit}  
sup = 0.0  
e_sup = 0.0  
p_sup = 0.0  
lb = 5.0  
ub = 0.0 
parent = None  
children = [] 
avg_weight = 0.65

node = Node[Item, Transaction](item_set, sup, e_sup, p_sup, lb, ub, parent, children, avg_weight)



print(node)