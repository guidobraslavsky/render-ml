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

    # Enviar fotos si existen
    fotos = data.get("fotos", [])
    for foto in fotos:
        send_photo(foto)

    return jsonify({"status": "ok"}), 200

def send_photo(photo_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": photo_url
    }
    requests.post(url, json=payload)
