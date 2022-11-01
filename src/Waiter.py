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
        while True:
            order = self.tables.waiter_has_order_to_serve(self.id)
            if order is not None:
                self.serve_order(order['table_id'])
            elif self.tables.get_tables_with_no_orders():
                time.sleep(random.randint(10, 30))
                self.tables.tables_mutex.acquire()
                self.look_for_order()
                self.tables.tables_mutex.release()
            else:
                time.sleep(2)


    def look_for_order(self):
        order = self.tables.get_order()
        if order != {} :
            order["waiter_id"] = self.id
            time.sleep(random.randint(2, 4))
            order["pick_up_time"] = time.time()
            send_order_to_kitchen(order)


    def serve_order(self, table_id):
        self.tables.serve_order(table_id)
