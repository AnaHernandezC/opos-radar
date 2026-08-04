import requests
from config import TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID
def send(msg):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                  json={"chat_id":TELEGRAM_CHAT_ID,"text":msg},
                  timeout=30).raise_for_status()
