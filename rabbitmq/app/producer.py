import pika
import json
import time
import requests
from datetime import datetime, timedelta
from .settings import CURRENCY_LIST, API_KEY_PATH, DELAY


API_URL = "https://api.apilayer.com/fixer/latest"
API_PARAMS = {
    "base": "RUB",
    "symbols": ",".join(CURRENCY_LIST)
}


def read_key():
    with open(API_KEY_PATH) as file:
        key = file.readline()
    return key


def headers():
    return {"apikey": read_key()}


def produce(connection: pika.BlockingConnection):
    channel = connection.channel()
    response = requests.get(API_URL, params=API_PARAMS, headers=headers())
    content = json.loads(response.text)
    rates = content["rates"]
    channel.basic_publish(
        exchange='test', routing_key="queue_key", body=json.dumps(rates)
    )


def main():
    con_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(con_params)
    t = datetime.strptime(DELAY, "%H:%M:%S")
    dt = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    try:
        while True:
            produce(connection)
            time.sleep(dt.total_seconds())
    except KeyboardInterrupt:
        pass
    connection.close()


if __name__ == "__main__":
    main()
