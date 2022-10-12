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

@app.route('/distribution', methods=['POST'])
def receive_order():
    data = request.json
    app.logger.info("Order is ready!")

    data = json.loads(data)
    app.logger.info(f"ORDER BACK FROM THE KICHEN: {data}")
    tables.prepared_foods_q.append(data)
    tables.calculate_rating_based_on_cooking_time(data)

    return "Ok"

if __name__ == '__main__':
    tables = Tables(10)

    app.run(debug=True, port=5001, host="0.0.0.0")
