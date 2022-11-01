import queue
import random
import threading

from src.Table import Table


def get_nr_of_stars(order):
    if order['cooking_time'] < order['max_wait']:
        return 5
    elif order['cooking_time'] < order['max_wait'] * 1.1:
        return 4
    elif order['cooking_time'] < order['max_wait'] * 1.2:
        return 3
    elif order['cooking_time'] < order['max_wait'] * 1.3:
        return 2

    return 1


class Tables:

    def __init__(self, nr_of_tables):
        self.nr_of_tables = nr_of_tables
        self.tables = []
        self.tables_mutex = threading.Lock()
        self.tables_order_mutex = threading.Lock()
        self.prepared_foods_q = []
        self.orders = 0
        self.rating = 0
        self.allraiting = 0

        for table_id in range(1, self.nr_of_tables + 1):
            self.tables.append(Table(table_id))

    def get_order(self):
        random_table_with_no_order = self.__get_random_table_with_no_order()
        order = {}

        if random_table_with_no_order:
            random_table_with_no_order.make_order()
            order = random_table_with_no_order.get_order()

        return order

    def waiter_has_order_to_serve(self, waiter_id):
        for order in self.prepared_foods_q:
            print(order)
            if order["waiter_id"] == waiter_id:
                self.prepared_foods_q.remove(order)
                print(f'Order is sent to the table {order["table_id"]}')
                return order
            else:
                return None

    def serve_order(self, table_id):
        table = self.get_table_with_id(table_id)
        table.receive_order()

    def get_table_with_id(self, table_id):
        for table in self.tables:
            if table.id[0] == int(table_id):
                return table

        return {}

    def __get_random_table_with_no_order(self):
        tables_with_no_order = self.get_tables_with_no_orders()

        if tables_with_no_order:
            random_index = random.randint(0, len(tables_with_no_order) - 1)

            return tables_with_no_order[random_index]

        return {}

    def get_tables_with_no_orders(self):
        with_no_orders = []

        for table in self.tables:
            if not table.has_placed_order:
                with_no_orders.append(table)

        return with_no_orders

    def calculate_rating_based_on_cooking_time(self, order):
        self.orders += 1
        nr_of_stars = get_nr_of_stars(order)
        if self.orders is not 1:
            self.allraiting = self.allraiting + nr_of_stars
            self.rating = self.allraiting / self.orders
        else:
            self.allraiting = nr_of_stars
            self.rating = nr_of_stars
        print(f'Rating: {self.rating}, nr of orders {self.orders}')
        print(f'Last order rating: {nr_of_stars}  time waited: {order["cooking_time"]} for max-wait: {order["max_wait"]} order items: {len(order["items"])}')