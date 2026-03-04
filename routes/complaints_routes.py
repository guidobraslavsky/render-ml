from flask import Blueprint, request, jsonify, render_template
from config import Config
from services.telegram_service import send_telegram, send_photo
from services.ml_service import get_order, reply_to_buyer
from services.email_service import send_email
from database import guardar_reclamo, obtener_reclamo

complaint_bp = Blueprint("complaint", __name__)


@complaint_bp.route("/")
def form():
    return render_template("form.html")


@complaint_bp.route("/complaint", methods=["POST"])
def complaint():
    data = request.form

    if request.headers.get("X-Secret-Key") != Config.SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    order_id = data.get("pedido_ml")

    order = get_order(order_id)

    if order:
        buyer = order.get("buyer", {})
        print("Comprador:", buyer)

    try:
        reply_to_buyer(
            order_id, "Hola 👋 Recibimos tu reclamo y ya estamos revisando el caso."
        )
    except Exception as e:
        print("Error respondiendo en ML:", e)

    reclamo_id = guardar_reclamo(data)

    print("Enviando Telegram...")

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

    fotos = request.files.getlist("fotos")
    for foto in fotos:
        send_photo(foto)

    try:
        send_email(
            data.get("contacto"),
            data.get("nombre"),
            data.get("pedido_ml"),
            data.get("producto"),
            reclamo_id,
        )
        print("Email enviado correctamente")
    except Exception as e:
        print("Error enviando email:", e)

    return jsonify({"status": "ok"}), 200


@complaint_bp.route("/order/<order_id>")
def order_info(order_id):

    order = get_order(order_id)

    if not order:
        return {"error": "Orden no encontrada"}, 404

    item = order["order_items"][0]["item"]

    buyer = order["buyer"]

    return {"producto": item["title"], "comprador": buyer["nickname"]}


@complaint_bp.route("/reclamo/<int:reclamo_id>")
def ver_reclamo(reclamo_id):

    reclamo = obtener_reclamo(reclamo_id)

    if not reclamo:
        return "Reclamo no encontrado", 404

    return render_template("reclamo.html", reclamo=reclamo)
