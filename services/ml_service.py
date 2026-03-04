import requests
import os
from services.ml_token_service import get_access_token

ML_TOKEN = os.environ.get("ML_ACCESS_TOKEN")


def get_order(order_id):

    token = get_access_token()

    url = f"https://api.mercadolibre.com/orders/{order_id}"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()

    return None


def reply_to_buyer(order_id, message):

    url = f"https://api.mercadolibre.com/messages/orders/{order_id}"

    headers = {
        "Authorization": f"Bearer {ML_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {"text": message}

    r = requests.post(url, headers=headers, json=payload)

    print("ML reply status:", r.status_code)
    print("ML reply response:", r.text)
