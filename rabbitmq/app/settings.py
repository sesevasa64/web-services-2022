import os


API_KEY_PATH = "key.txt"
CURRENCY_LIST = ["EUR", "USD"]
DELAY = "00:01:00"
SMTP_SERVER_HOST = "smtp.gmail.com"
SMTP_SERVER_PORT = 587
SMTP_LOGIN = os.getenv("SMTP_LOGIN")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SUBSCRIBED_EMAIL_LIST = ["370759@edu.itmo.ru"]
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
