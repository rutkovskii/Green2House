from flask import abort, request, Blueprint, render_template, session, flash, jsonify
from flask_login import login_required
from app.database.models import DataSample
from app.database.database import session_scope
from app.user.config import UserConfig

from datetime import datetime, timedelta
from flask import jsonify


from app.server_logger import setup_logger, log_errors

charts_page_bp = Blueprint("charts_page_bp", __name__)

logger = setup_logger(__name__, "server.log")


@charts_page_bp.route(UserConfig.CHARTS_ROUTE, methods=["GET"])
@log_errors(logger)
@login_required
def charts():
    """Render the charts page."""
    return render_template("user_charts.html", title="Charts — G2H")


@charts_page_bp.route(UserConfig.SERVE_GRAPH_DATA_ROUTE, methods=["GET"])
@log_errors(logger)
@login_required
def get_data_samples():
    now = datetime.now()
    duration = request.args.get("duration", "24h")

    if duration == "24h":
        past_day = now - timedelta(days=1)
    else:
        past_day = datetime.min

    user_id = request.args.get("user_id")

    logger.info(f"User ID: {user_id}")

    if not request.args.get("token"):
        return abort(403)

    data_samples_dicts = []
    if user_id:
        with session_scope() as s:
            data_samples = (
                s.query(DataSample)
                .filter(DataSample.user_id == user_id)
                .filter(DataSample.timestamp >= past_day)
                .filter(DataSample.timestamp <= now)
                .order_by(DataSample.timestamp.asc())
                .all()
            )
            data_samples_dicts = [sample.to_dict_charts() for sample in data_samples]
    else:
        with session_scope() as s:
            data_samples = (
                s.query(DataSample)
                .filter(DataSample.timestamp >= past_day)
                .filter(DataSample.timestamp <= now)
                .order_by(DataSample.timestamp.asc())
                .all()
            )
            data_samples_dicts = [sample.to_dict_charts() for sample in data_samples]

    return jsonify(data_samples_dicts)
