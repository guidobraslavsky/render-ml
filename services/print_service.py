import subprocess
import requests
import time

PRINTER_NAME = "XP410B"


def imprimir_zpl(zpl):

    try:

        subprocess.run(
            ["lpr", "-P", PRINTER_NAME, "-o", "raw"], input=zpl.encode(), check=True
        )

        print("Etiqueta enviada a impresora")

    except Exception as e:

        print("Error imprimiendo:", e)
