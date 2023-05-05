from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

home_page_bp = Blueprint("home_bp", __name__)


@home_page_bp.route("/home")
@login_required
def home():
    if current_user.is_admin:
        return redirect(url_for("admin_bp.serve_admin_main"))
    return render_template("/user_home_page.html", title="Home — G2H")
