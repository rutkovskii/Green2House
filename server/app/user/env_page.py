from flask import request, Blueprint, render_template, session, flash, jsonify
from flask_login import login_required
from datetime import datetime as dt
import requests
import json
from app.database.models import Instructions
from app.database.database import session_scope
from app.user.config import UserConfig
from app.user.vegetables import Plants

from app.server_logger import setup_logger, log_errors

env_page_bp = Blueprint("env_page_bp", __name__)

logger = setup_logger(__name__, "server.log")


@env_page_bp.route(UserConfig.BUTTONS_ROUTE, methods=["GET", "POST"])
@log_errors(logger)
@login_required
def buttons():
    """"""

    # if request.method == "POST":
    #     data = request.get_json()
    #     is_pressed = data.get("is_pressed", False)
    #     print(f'Button is now: {"pressed" if is_pressed else "not pressed"}')

    #     if is_pressed:
    #         body = json.dumps({"user_id": session.get("user_id"), "water": True})
    #     else:
    #         body = json.dumps({"user_id": session.get("user_id"), "water": False})

    #     headers = {"Content-type": "application/json", "Accept": "text/plain"}

    #     try:
    #         r = requests.post(UserConfig.WATER_URL, json=body, headers=headers)
    #     except requests.exceptions.ConnectionError as e:
    #         print(e)
    #         return jsonify({"success": False})

    #     print(f"Status Code: {r.status_code}, Response: {r.json()}")

    #     return jsonify({"success": True})

    return render_template("user_buttons.html", title="Buttons")


@env_page_bp.route(UserConfig.ENV_ROUTE, methods=["GET", "POST"])
@log_errors(logger)
@login_required
def set_environment():
    if request.method == "POST":
        now = dt.now()
        print(request.form.get("watering_time"))
        print(request.form.get("watering_duration"))

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
        r = requests.post(UserConfig.INSTRUCTIONS_URL, json=body, headers=headers)

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

        if r.status_code == 200:
            flash("Environment settings updated successfully", "success")
        else:
            print(r.status_code)
            print(r)
            flash("Environment settings could not be updated", "danger")

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
        title="Set ENV — Green2House",
    )
