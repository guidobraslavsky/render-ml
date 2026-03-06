import segno

BASE_URL = "https://render-ml-automation.onrender.com"


def generar_sticker(order_id):

    url = f"{BASE_URL}/form?order={order_id}"

    qr = segno.make(url)

    matrix = qr.matrix

    zpl_qr = ""

    size = 6  # tamaño del módulo del QR
    start_x = 50
    start_y = 100

    y = start_y

    for row in matrix:

        x = start_x

        for col in row:

            if col:
                zpl_qr += f"^FO{x},{y}^GB{size},{size},{size}^FS\n"

            x += size

        y += size

    zpl = f"""
^XA
^PW800
^LL1200

^FO50,40
^A0N,40,40
^FDSoporte Pedido ML^FS

{zpl_qr}

^FO50,750
^A0N,35,35
^FDEscanea si hay un problema^FS

^XZ
"""

    return zpl
