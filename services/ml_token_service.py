import time
import requests
import os

ML_CLIENT_ID = os.environ.get("ML_CLIENT_ID")
ML_CLIENT_SECRET = os.environ.get("ML_CLIENT_SECRET")
ML_REFRESH_TOKEN = os.environ.get("ML_REFRESH_TOKEN")

ACCESS_TOKEN = None
EXPIRES_AT = 0


def get_access_token():
    global ACCESS_TOKEN, EXPIRES_AT

    # si el token sigue válido
    if ACCESS_TOKEN and time.time() < EXPIRES_AT - 300:
        return ACCESS_TOKEN

    print("🔄 Renovando access token ML...")

    url = "https://api.mercadolibre.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": ML_CLIENT_ID,
        "client_secret": ML_CLIENT_SECRET,
        "refresh_token": ML_REFRESH_TOKEN,
    }

    r = requests.post(url, data=data)

    if r.status_code != 200:
        print("❌ Error ML token:", r.text)
        raise Exception("Error obteniendo access token")

    token_info = r.json()

    ACCESS_TOKEN = token_info["access_token"]
    EXPIRES_AT = time.time() + token_info["expires_in"]

    print("✅ Token ML actualizado")

    return ACCESS_TOKEN
