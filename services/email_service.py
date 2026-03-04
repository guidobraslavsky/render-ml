import requests
import os

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")


def send_email(destinatario, nombre, pedido, producto, reclamo_id):

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    link = f"https://render-ml-automation.onrender.com/reclamo/{reclamo_id}"

    data = {
        "from": "Soporte <onboarding@resend.dev>",
        "to": [destinatario],
        "subject": f"Recibimos tu reclamo #{reclamo_id}",
        "html": f"""
        <h2>Recibimos tu reclamo</h2>

        <p>Hola <b>{nombre}</b>,</p>

        <p>Tu reclamo fue registrado correctamente.</p>

        <h3>Datos del caso</h3>

        <ul>
        <li><b>Número de caso:</b> {reclamo_id}</li>
        <li><b>Pedido ML:</b> {pedido}</li>
        <li><b>Producto:</b> {producto}</li>
        </ul>

        <p>Puedes ver el estado de tu reclamo aquí:</p>

        <p>
        <a href="{link}">
        Ver estado del reclamo
        </a>
        </p>

        <hr>

        <p>Equipo de soporte</p>
        """,
    }

    requests.post(url, headers=headers, json=data)


def send_email_resuelto(destinatario, nombre, reclamo_id):

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    link = f"https://render-ml-automation.onrender.com/reclamo/{reclamo_id}"

    data = {
        "from": "Soporte <onboarding@resend.dev>",
        "to": [destinatario],
        "subject": f"Tu reclamo #{reclamo_id} fue resuelto",
        "html": f"""
        <h2>Reclamo resuelto</h2>

        <p>Hola {nombre},</p>

        <p>Tu reclamo <b>#{reclamo_id}</b> fue resuelto.</p>

        <p>Si necesitas más ayuda puedes revisar tu caso aquí:</p>

        <p>
        <a href="{link}">
        Ver reclamo
        </a>
        </p>

        <p>Gracias por contactarnos.</p>
        """,
    }

    requests.post(url, headers=headers, json=data)
