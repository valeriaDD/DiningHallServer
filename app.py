import json
import logging

from flask import Flask, request
from pipenv.patched.pip._vendor import requests

from src.Tables import Tables
from src.Waiter import Waiter
from src.constants import NR_OF_TABLES, NR_OF_WAITERS

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')



@app.route("/")
def miaw():
    return "Hello from dining hall server"

@app.route("/get")
def home():
    for waiter_id in range (NR_OF_WAITERS):
        waiter = Waiter(waiter_id, tables)
        waiter.daemon = True # Daemon thread dies when main thread dies
        waiter.start()

    return "Sent!"

@app.route('/order-from-kitchen', methods=['POST'])
def receive_order():
    data = request.json
    app.logger.info("Order is ready!")

    table_id = json.loads(data)["id"]
    app.logger.info(f"Table info {json.dumps(tables.get_table_with_id(table_id[0]).get_table())}")

    tables.serve_order(table_id[0])

    app.logger.info("Order served!")
    app.logger.info(f"Table info {json.dumps(tables.get_table_with_id(table_id[0]).get_table())}")

    return "Ok"

@app.route("/get-tables")
def get_all_tables_info():
    return tables.get_all_tables()

@app.route("/get-table")
def get_table():
    table_id =  request.args.get('id')
    table = tables.get_table_with_id(table_id)
    return json.dumps(table)


if __name__ == '__main__':
    tables = Tables(NR_OF_TABLES)

    app.run(debug=True, port=5001, host="0.0.0.0")