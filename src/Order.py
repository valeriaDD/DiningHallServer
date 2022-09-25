import itertools
import random

from src.Menu import Menu


class Order:
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(Order.id_iter) + 1
        self.max_wait = 0
        self.priority = 1
        self.order_items = []

    def make_order(self):
        self.__set_order_priority()
        self.__set_menu_items()

        order = {
            "id": self.id,
            "priority": self.priority,
            "max_wait": self.max_wait,
            "order_items": self.order_items
        }
        return order

    def __set_order_priority(self):
        self.priority = random.randint(1, 5)

    def __set_menu_items(self):
        items_number = random.randint(1, 8)

        for item in range(0, items_number):
            dish = Menu().get_random_menu_item()
            self.order_items.append(dish)
            self.__set_max_wait(dish.get("preparation-time"))

    def __set_max_wait(self, order_wait_time):
        if self.max_wait < order_wait_time * 1.3:
            self.max_wait = order_wait_time * 1.3
