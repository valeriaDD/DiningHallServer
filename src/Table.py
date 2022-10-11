import itertools
import threading

from src.Order import Order


class Table:
    id_iter = itertools.count()

    def __init__(self, table_id, has_placed_order=False):
        self.id = table_id,
        self.has_placed_order = has_placed_order
        self.order = {}

    def make_order(self):
        self.has_placed_order = True
        self.order = Order().make_order()
        self.order["table_id"] = self.id[0]

    def get_order(self):
        return self.order

    def receive_order(self):
        self.has_placed_order = False
        self.order = {}
        print(f'Table {self.id} received order')

