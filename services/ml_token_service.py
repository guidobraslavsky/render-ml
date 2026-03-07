import requests
import time
import os
import database

TOKEN_URL = "https://api.mercadolibre.com/oauth/token"


def get_access_token():

    token_data = database.get_token()

    if token_data:

        access_token = token_data["access_token"]
        expires_at = token_data["expires_at"]

        if time.time() < expires_at:
            return access_token

    return refresh_access_token()


def refresh_access_token():

    refresh_token = os.environ.get("ML_REFRESH_TOKEN")

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.environ.get("ML_CLIENT_ID"),
        "client_secret": os.environ.get("ML_CLIENT_SECRET"),
        "refresh_token": refresh_token,
    }

    r = requests.post(TOKEN_URL, data=payload)

    if r.status_code != 200:
        raise Exception("Error obteniendo access token")

    data = r.json()

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    expires_in = data["expires_in"]

    expires_at = time.time() + expires_in - 60

    database.save_token(access_token, refresh_token, expires_at)

    return access_token
