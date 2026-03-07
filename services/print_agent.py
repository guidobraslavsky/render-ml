import requests
import time
import subprocess

from services.ml_service import get_recent_orders
import database
from services.zpl_sticker_service import generar_sticker
from services.print_service import imprimir_zpl

SERVER_URL = "https://render-ml-automation.onrender.com"

printed_cache = set()

print("🚀 Print Agent iniciado")


def check_ml_orders():

    orders = get_recent_orders()

    for order in orders:

        order_id = str(order["order_id"])

        if database.order_exists(order_id):
            continue

        print("Nueva orden detectada:", order_id)

        database.insert_order(order_id)


def check_print_queue():

    try:

        r = requests.get(f"{SERVER_URL}/print_queue", timeout=30)

        if r.status_code != 200:
            print("Error servidor:", r.status_code)
            return

        data = r.json()

        orders = data.get("orders", [])

        if not orders:
            print("No hay órdenes pendientes")
            return

        for order in orders:

            order_id = order["order_id"]

            print("🖨 Imprimiendo orden:", order_id)

            zpl = generar_sticker(order_id)

            imprimir_zpl(zpl)

            requests.post(
                f"{SERVER_URL}/mark_printed", json={"order_id": order_id}, timeout=30
            )

    except Exception as e:

        print("Error en agente:", e)


while True:

    check_ml_orders()

    check_print_queue()

    time.sleep(15)
