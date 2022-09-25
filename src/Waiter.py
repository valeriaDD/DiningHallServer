import json
import random
import threading
import time

from pipenv.patched.pip._vendor import requests

from src.Tables import Tables
from src.constants import KITCHEN_URL


def send_order_to_kitchen(order):
    requests.post(f'{KITCHEN_URL}/order', json=json.dumps(order))
    print("Order is sent to the kitchen")


class Waiter(threading.Thread):
    def __init__(self, waiter_id , tables: Tables):
        super(Waiter, self).__init__()
        self.id = waiter_id
        self.tables = tables

    def run(self):
        while self.tables.get_tables_with_no_orders():
            time.sleep(random.randint(2,5))
            self.look_for_order()

    def look_for_order(self):
        order = self.tables.get_order()
        if order != "All full" :
            send_order_to_kitchen(order)

def serve_order(self, table_id):
        self.tables.serve_order(table_id)
