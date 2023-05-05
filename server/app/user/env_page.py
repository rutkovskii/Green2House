from flask import request, Blueprint, render_template, session, flash, jsonify
from flask_login import login_required
from datetime import datetime as dt
import requests
import json
from time import sleep

from app.database.models import Instructions
from app.database.database import session_scope
from app.user.config import UserConfig
from app.user.vegetables import Plants
from app.utils import class_to_dict

from app.server_logger import setup_logger, log_errors

env_page_bp = Blueprint("env_page_bp", __name__)

logger = setup_logger(__name__, "server.log")


@env_page_bp.route(UserConfig.BUTTONS_ROUTE, methods=["GET", "POST"])
@log_errors(logger)
@login_required
def buttons():
    """Render the buttons page."""
    return render_template("user_buttons.html", title="Buttons — G2H")


@env_page_bp.route(UserConfig.ENV_ROUTE, methods=["GET", "POST"])
@log_errors(logger)
@login_required
def set_environment():
    if request.method == "POST":
        now = dt.now()

        body = json.dumps(
            {
                "user_id": session.get("user_id"),
                "min_temperature": request.form.get("temperature_min"),
                "max_temperature": request.form.get("temperature_max"),
                "min_humidity": request.form.get("humidity_min"),
                "max_humidity": request.form.get("humidity_max"),
                "watering_time": request.form.get("watering_time"),
                "watering_duration": request.form.get("watering_duration"),
                "timestamp": str(now),
            }
        )
        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        success = False
        max_retries = 3
        retry_interval = 5  # seconds

        for _ in range(max_retries):
            try:
                r = requests.post(
                    UserConfig.INSTRUCTIONS_URL, json=body, headers=headers
                )

                if r.status_code == 200:
                    success = True
                    break
                else:
                    sleep(retry_interval)
            except Exception as e:
                logger.error(f"Error while sending request: {e}")
                sleep(retry_interval)

        if success:
            instructions = Instructions(
                user_id=session.get("user_id"),
                min_temperature=request.form.get("temperature_min"),
                max_temperature=request.form.get("temperature_max"),
                min_humidity=request.form.get("humidity_min"),
                max_humidity=request.form.get("humidity_max"),
                watering_time=request.form.get("watering_time"),
                watering_duration=request.form.get("watering_duration"),
                timestamp=now,
            )

            with session_scope() as s:
                s.add(instructions)

            flash("Environment settings updated successfully", "success")
        else:
            logger.error(f"Status Code: {r.status_code}, Response: {r.json()}")
            flash(
                "Greenhouse is disconnected, environment settings could not be updated",
                "danger",
            )

    # generate options for the watering_time dropdown
    watering_time_options = ""
    for h in range(0, 24):
        for m in range(0, 60, 15):
            watering_time_options += (
                f'<option value="{h:02d}:{m:02d}">{h:02d}:{m:02d}</option>'
            )

    # generate options for the watering_duration dropdown
    watering_duration_options = ""
    for s in range(5, 121, 5):
        watering_duration_options += f'<option value="{s}">{s} seconds</option>'

    return render_template(
        "user_env_page.html",
        watering_time_options=watering_time_options,
        watering_duration_options=watering_duration_options,
        title="Set Environment — Green2House",
        plants_data=json.dumps(class_to_dict(Plants)),
    )
