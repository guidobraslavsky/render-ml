import requests
from config import Config


def send_telegram(message):

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"

    payload = {"chat_id": Config.CHAT_ID, "text": message}

    r = requests.post(url, json=payload)

    print("Telegram status:", r.status_code)
    print("Telegram response:", r.text)


def send_photo(photo):

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendPhoto"

    files = {"photo": photo}

    data = {"chat_id": Config.CHAT_ID}

    requests.post(url, data=data, files=files)
