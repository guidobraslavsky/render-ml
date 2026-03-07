from dotenv import load_dotenv
from flask import Flask, request
from routes.complaints_routes import complaint_bp
from routes.admin_routes import admin_bp
import database
from database import init_db
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

init_db()


@app.route("/")
def home():
    return "Servidor funcionando"


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/print_queue")
def print_queue():

    orders = database.get_orders_pending_print()

    return {"orders": orders}


@app.route("/mark_printed", methods=["POST"])
def mark_printed():

    data = request.json

    order_id = data["order_id"]

    database.mark_order_printed(order_id)

    return {"status": "ok"}


app.register_blueprint(admin_bp)
app.register_blueprint(complaint_bp)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
