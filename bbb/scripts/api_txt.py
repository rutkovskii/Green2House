from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import Instructions
from database.database import session_scope
from datetime import datetime
import json


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


latest_instructions = {
    # button actions
    "shutdown": False,
    "water": False,
    "mist": False,
    "lid": False,
    "fan": False,
    "heat": False,
    # instructions
    "min_temperature": None,
    "max_temperature": None,
    "min_humidity": None,
    "max_humidity": None,
    "watering_time": None,
    "watering_duration": None,
    "timestamp": None,
    "updated": False,
}

def write_instructions_to_file(filename, latest_instructions):
    with open(filename, 'w') as f:
        json.dump(latest_instructions, f)


import os

def write_instructions_to_file(filename, latest_instructions):
    try:
        # Check if the directory exists, if not create it
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(filename, 'w') as f:
            json.dump(latest_instructions, f)
    except PermissionError:
        print(f"Permission denied: Can't write to the file {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.route("/shutdown", methods=["POST"])
def shutdown_system():
    if request.method == "POST":
        body = request.get_json()

        global latest_instructions
        latest_instructions["shutdown"] = body["shutdown"]

        # Perform necessary actions to shut down the system

        print("System shut down", flush=True)

        # Write to file
        write_instructions_to_file('latest_instructions.txt', latest_instructions)

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

        write_instructions_to_file('latest_instructions.txt', latest_instructions)

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

        write_instructions_to_file('latest_instructions.txt', latest_instructions)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
