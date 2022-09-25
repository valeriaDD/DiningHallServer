import json
import random

from src.Table import Table


class Tables:

    def __init__(self, nr_of_tables):
        self.nr_of_tables = nr_of_tables
        self.tables = []

        for table_id in range(1, self.nr_of_tables + 1):
            self.tables.append(Table(table_id))

    def get_all_tables(self):
        all_tables = []
        for item in self.tables:
            all_tables.append(item.get_table())

        return json.dumps(all_tables)

    def get_order(self):
        random_table_with_no_order = self.__get_random_table_with_no_order()

        if random_table_with_no_order:
            random_table_with_no_order.make_order()
            return random_table_with_no_order.get_table()

        return "All full"

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
