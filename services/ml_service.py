import requests
import os

from services.ml_token_service import get_access_token
from services.zpl_sticker_service import generar_sticker
from services.print_service import imprimir_zpl


ML_TOKEN = os.environ.get("ML_ACCESS_TOKEN")


def get_order(order_id):

    token = get_access_token()

    url = f"https://api.mercadolibre.com/orders/{order_id}"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Error obteniendo orden:", r.status_code)
        return None

    return r.json()


def get_recent_orders():

    token = get_access_token()

    url = "https://api.mercadolibre.com/orders/search?seller=me&sort=date_desc"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Error obteniendo órdenes:", r.status_code)
        return []

    data = r.json()

    orders = []

    for o in data["results"]:

        orders.append({"order_id": o["id"], "shipping_id": o["shipping"]["id"]})

    return orders


def get_shipping_label(shipment_id):

    token = get_access_token()

    url = f"https://api.mercadolibre.com/shipment_labels?shipment_ids={shipment_id}&response_type=zpl"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Error descargando etiqueta:", r.status_code)
        return None

    return r.text


def combinar_etiqueta(label_zpl, qr_zpl):

    label_zpl = label_zpl.replace("^XZ", "")

    return f"""
{label_zpl}

^FO50,650
^A0N,30,30
^FDSoporte post venta^FS

{qr_zpl}

^XZ
"""


def imprimir_etiqueta_con_qr(order_id):

    order = get_order(order_id)

    if not order:
        return

    shipment_id = order["shipping"]["id"]

    label_zpl = get_shipping_label(shipment_id)

    if not label_zpl:
        return

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
