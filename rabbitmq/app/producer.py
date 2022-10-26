import pika
import json
import time
import requests
from datetime import datetime, timedelta
from pika.adapters.blocking_connection import BlockingChannel
from .settings import CURRENCY_LIST, API_KEY_PATH, DELAY
from .utils import create_logger
from typing import Dict


logger = create_logger("producer")


API_URL = "https://api.apilayer.com/fixer/latest"
API_PARAMS = {
    "base": "RUB",
    "symbols": ",".join(CURRENCY_LIST)
}


def read_key() -> str:
    """Read key from txt file

    Returns:
        str: api key for fixer.io
    """
    with open(API_KEY_PATH) as file:
        key = file.readline()
    return key


def headers() -> Dict[str, str]:
    """Get headers for fixer.io api

    Returns:
        Dict[str, str]: api headers
    """
    return {"apikey": read_key()}


def get_exchange_rates():
    """Connect to fixer.io and get exchange rates

    Returns:
        Dict[str, int]: (currancy_name, rate) dictionary
    """
    response = requests.get(API_URL, params=API_PARAMS, headers=headers())
    content = json.loads(response.text)
    rates = content["rates"]
    return rates


def produce(channel: BlockingChannel, rates: Dict[str, int]):
    """Publish new exchange rates to queue

    Args:
        channel (BlockingChannel): pika channel
        rates (Dict[str, int]): new exchange rates
    """
    channel.basic_publish(
        exchange='test', routing_key="queue_key", body=json.dumps(rates)
    )
    logger.debug(f"Added message to queue with content {rates}")


def main():
    """Setup pika and start producer loop
    """
    con_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(con_params)
    channel = connection.channel()
    t = datetime.strptime(DELAY, "%H:%M:%S")
    dt = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    logger.debug("Producer service started")
    try:
        while True:
            rates = get_exchange_rates()
            produce(channel, rates)
            time.sleep(dt.total_seconds())
    except KeyboardInterrupt:
        pass
    connection.close()
    logger.debug("Producer service ended")


if __name__ == "__main__":
    main()
