from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from flask_login import current_user
from app.admin.config import AdminConfig

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home_bp.home"))

    return render_template("index.html", title="G2H")


@index_bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        AdminConfig.FLASK_STATIC_DIR,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
