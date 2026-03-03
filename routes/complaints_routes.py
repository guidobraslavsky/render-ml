from flask import Blueprint, request, jsonify, render_template
from config import Config
from services.telegram_service import send_telegram, send_photo
from database import guardar_reclamo

complaint_bp = Blueprint("complaint", __name__)


@complaint_bp.route("/")
def form():
    return render_template("form.html")


@complaint_bp.route("/complaint", methods=["POST"])
def complaint():
    data = request.json

    if request.headers.get("X-Secret-Key") != Config.SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    reclamo_id = guardar_reclamo(data)

    message = f"""
🚨 NUEVO RECLAMO #{reclamo_id}

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
