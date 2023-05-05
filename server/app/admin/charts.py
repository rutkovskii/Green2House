from flask import abort, request, Blueprint, render_template, session, flash, jsonify
from flask_login import login_required
from app.database.database import session_scope
from app.admin.config import AdminConfig
from app.server_logger import setup_logger, log_errors

admin_charts_page_bp = Blueprint("admin_charts_page_bp", __name__)

logger = setup_logger(__name__, "server.log")


@admin_charts_page_bp.route(AdminConfig.ADMIN_PAGE_CHARTS_ROUTE, methods=["GET"])
@log_errors(logger)
@login_required
def charts():
    """Render the charts page."""
    return render_template("admin_charts.html", title="Admin Charts — Green2House")
