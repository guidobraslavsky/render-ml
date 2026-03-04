from flask import Blueprint, render_template, redirect, request, session
from database import obtener_reclamos, marcar_resuelto, obtener_reclamo
from services.email_service import send_email_resuelto
import os

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        admin_user = os.environ.get("ADMIN_USER")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        print("Usuario ingresado:", username)
        print("Password ingresado:", password)
        print("ADMIN_USER:", admin_user)
        print("ADMIN_PASSWORD:", admin_password)

        if username == admin_user and password == admin_password:
            session["admin_logged"] = True
            return redirect("/admin")

    return render_template("login.html", error=True)


@admin_bp.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login")


@admin_bp.route("/admin")
def admin_panel():
    if not session.get("admin_logged"):
        return redirect("/admin/login")

    reclamos = obtener_reclamos()
    return render_template("admin.html", reclamos=reclamos)


@admin_bp.route("/admin/resolver/<int:reclamo_id>")
def resolver_reclamo(reclamo_id):

    if not session.get("admin_logged"):
        return redirect("/admin/login")

    reclamo = obtener_reclamo(reclamo_id)

    marcar_resuelto(reclamo_id)

    try:

        send_email_resuelto(reclamo["contacto"], reclamo["nombre"], reclamo_id)

        print("Email de resolución enviado")

    except Exception as e:

        print("Error enviando email:", e)

    return redirect("/admin")
