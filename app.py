from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SECRET_KEY = os.environ.get("FORM_SECRET")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload, timeout=5)

def send_photo(photo_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "photo": photo_url}
    requests.post(url, json=payload, timeout=5)

@app.route("/complaint", methods=["POST"])
def complaint():
    data = request.json

    # 🔐 Validación de seguridad
    if data.get("secret") != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    message = f"""
🚨 NUEVO RECLAMO

👤 Nombre: {data.get('nombre')}
📦 Pedido ML: {data.get('pedido_ml')}
📱 Contacto: {data.get('contacto')}
📦 Producto: {data.get('producto')}
⚠ Tipo: {data.get('tipo')}

📝 Descripción:
{data.get('descripcion')}
"""

    send_telegram(message)

    fotos = data.get("fotos", [])
    for foto in fotos:
        send_photo(foto)

    return jsonify({"status": "ok"}), 200
