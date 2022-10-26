import pika
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .settings import (
    SMTP_SERVER_HOST, SMTP_SERVER_PORT, SMTP_LOGIN, SMTP_PASSWORD,
    SUBSCRIBED_EMAIL_LIST
)
from .utils import create_logger
from typing import Dict


logger = create_logger("consumer")


def exchange_rates_dict_to_text(data: Dict[str, int]) -> str:
    """Convert exchange rates to nice formatted text

    Args:
        data (Dict[str, int]): exchange rates

    Returns:
        str: formatted text
    """
    return "".join([f"{key}: {val}\n" for key, val in data.items()])


def send_email(email_to: str, data: str):
    """Send message to specific email

    Args:
        email_to (str): user email
        data (str): message content
    """
    message = MIMEMultipart()
    message["From"] = SMTP_LOGIN
    message["To"] = email_to
    message['Subject'] = "Exchange rates"
    message.attach(MIMEText(data, 'plain'))
    with smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT) as smtp_server:
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(SMTP_LOGIN, SMTP_PASSWORD)
        smtp_server.sendmail(SMTP_LOGIN, email_to, message.as_string())
    logger.debug(f"Succecfully sent email notification to {email_to}")


def consume(channel, method, properties, body):
    """Get exchange rates from queue
    """
    rates = json.loads(body)
    logger.debug(f"Received message from queue with content {rates}")
    for email in SUBSCRIBED_EMAIL_LIST:
        data = exchange_rates_dict_to_text(rates)
        send_email(email, data)


def main():
    """Setup pika and start consuming
    """
    con_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(con_params)
    channel = connection.channel()
    channel.basic_consume(
        queue='queue', auto_ack=True, on_message_callback=consume
    )
    logger.debug("Consumer service started")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    connection.close()
    logger.debug("Consumer service ended")


if __name__ == "__main__":
    main()
