from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import Instructions
from database.database import session_scope
from datetime import datetime
import json


def create_app(latest_instructions):
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})


    @app.route("/shutdown", methods=["POST"])
    def shutdown_system():
        if request.method == "POST":
            body = request.get_json()

            global latest_instructions
            latest_instructions["shutdown"] = body["shutdown"]

            # Perform necessary actions to shut down the system

            print("System shut down", flush=True)

            return jsonify({"message": "System shut down successfully"})

        return jsonify({"error": "Request must be JSON"})


    @app.route("/buttons", methods=["POST"])
    def buttons():
        if request.method == "POST":
            body = request.get_json()

            global latest_instructions
            action = body["action"]
            latest_instructions[action] = True
            latest_instructions["shutdown"] = True

            print(f"{action.capitalize()} action performed", flush=True)

            return jsonify(
                {"message": f"{action.capitalize()} action will be performed"}
            )

        return jsonify({"error": "Request must be JSON"})


    @app.route("/instructions", methods=["POST"])
    def instructions():
        if request.method == "POST":
            print("instructions")
            data = json.loads(request.get_json())
            print(data)
            date_string = data["timestamp"]
            date_format = "%Y-%m-%d %H:%M:%S.%f"

            datetime_object = datetime.strptime(date_string, date_format)
            timestamp = datetime_object.timestamp()

            data["timestamp"] = datetime.fromtimestamp(timestamp)

            print(data)

            latest_instructions["min_temperature"] = data["min_temperature"]
            latest_instructions["max_temperature"] = data["max_temperature"]
            latest_instructions["min_humidity"] = data["min_humidity"]
            latest_instructions["max_humidity"] = data["max_humidity"]
            latest_instructions["watering_time"] = data["watering_time"]
            latest_instructions["watering_duration"] = data["watering_duration"]

            latest_instructions["updated"] = True

            instructions = Instructions(
                user_id=data.get("user_id"),
                min_temperature=data.get("min_temperature"),
                max_temperature=data.get("max_temperature"),
                min_humidity=data.get("min_humidity"),
                max_humidity=data.get("max_humidity"),
                watering_time=data.get("watering_time"),
                watering_duration=data.get("watering_duration"),
                timestamp=data.get("timestamp"),
            )

            with session_scope() as s:
                s.add(instructions)

            return jsonify({"message": "OK"})

        return jsonify({"error": "Request must be JSON"})


    @app.route("/", methods=["GET"])
    def hello():
        return "Hello from BBB"

    return app
