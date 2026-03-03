from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

@app.route("/complaint", methods=["POST"])
def complaint():
    data = request.json

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

    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "Service running", 200
