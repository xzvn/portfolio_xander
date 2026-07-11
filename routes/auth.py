from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Jika sudah login, langsung menuju dashboard.
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not username or not password:
            flash(
                "Username dan password wajib diisi.",
                "warning",
            )
            return render_template(
                "auth/login.html",
                username=username,
            )

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(
            user.password_hash,
            password,
        ):
            flash(
                "Username atau password tidak sesuai.",
                "danger",
            )
            return render_template(
                "auth/login.html",
                username=username,
            )

        if user.role != "admin":
            flash(
                "Akun ini tidak memiliki akses sebagai admin.",
                "danger",
            )
            return render_template(
                "auth/login.html",
                username=username,
            )

        login_user(user, remember=remember)

        flash(
            f"Selamat datang, {user.username}.",
            "success",
        )

        return redirect(url_for("admin.dashboard"))

    return render_template("auth/login.html")


@auth_bp.get("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash(
            "Anda berhasil keluar dari halaman admin.",
            "success",
        )

    return redirect(url_for("auth.login"))