import pika
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .settings import (
    SMTP_SERVER_HOST, SMTP_SERVER_PORT, SMTP_LOGIN, SMTP_PASSWORD,
    SUBSCRIBED_EMAIL_LIST
)


def dict_to_text(data):
    return "".join([f"{key}: {val}\n" for key, val in data.items()])


def send_email(email_to, data):
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


def callback(channel, method, properties, body):
    rates = json.loads(body)
    print(rates)
    for email in SUBSCRIBED_EMAIL_LIST:
        data = dict_to_text(rates)
        send_email(email, data)


def main():
    con_params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(con_params)
    channel = connection.channel()
    channel.basic_consume(
        queue='queue', auto_ack=True, on_message_callback=callback
    )
    try:
        channel.start_consuming()
    except pika.exceptions.ConnectionClosedByBroker:
        pass
    connection.close()


if __name__ == "__main__":
    main()
