import requests
import os
from services.ml_token_service import get_access_token
from services.qr_service import generar_qr
from services.zpl_sticker_service import generar_sticker
from services.print_agent import imprimir_zpl


ML_TOKEN = os.environ.get("ML_ACCESS_TOKEN")


import requests

from services.ml_token_service import get_access_token
from services.zpl_sticker_service import generar_sticker


def get_order(order_id):

    token = get_access_token()

    url = f"https://api.mercadolibre.com/orders/{order_id}"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code == 200:

        order = r.json()

        print("Orden recibida:", order_id)

        zpl = generar_sticker(order_id)

        imprimir_zpl(zpl)

        print("Sticker enviado a impresora")

        return order

    else:

        print("Error obteniendo orden:", r.status_code)

    return None


def get_shipping_label(shipment_id):

    token = get_access_token()

    url = f"https://api.mercadolibre.com/shipment_labels?shipment_ids={shipment_id}&response_type=zpl"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.text

    return None


def imprimir_etiqueta_con_qr(order_id):

    order = get_order(order_id)

    shipment_id = order["shipping"]["id"]

    label_zpl = get_shipping_label(shipment_id)

    qr_zpl = generar_sticker(order_id)

    final_zpl = combinar_etiqueta(label_zpl, qr_zpl)

    imprimir_zpl(final_zpl)


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
