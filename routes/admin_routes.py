from flask import Blueprint, render_template, redirect, request, session
from database import obtener_reclamos, marcar_resuelto
import os

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == admin_password:
            session["admin_logged"] = True
            return redirect("/admin")

    return render_template("login.html")


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

    marcar_resuelto(reclamo_id)
    return redirect("/admin")
