from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home_bp.home"))

    return render_template("index.html", title="Green2House")
