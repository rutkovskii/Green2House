from flask import Flask, request
from database.models import Instructions
from database.database import session_scope
import json


app = Flask(__name__)


@app.route('/water-plant', methods=['POST'])
def water_plant():
    if request.method == 'POST':
        body = json.loads(request.get_json())

        print(body)

        return {"message": "JSON received"}, 200

    return {"error": "Request must be JSON"}, 415


@app.route('/instructions', methods=['POST'])
def instructions():
    if request.method == 'POST':
        body = json.loads(request.get_json())

        print(body)

        instructions = Instructions(
            user_id=body.get('user_id'),
            min_temperature=body.get('min_temperature'),
            max_temperature=body.get('max_temperature'),
            min_humidity=body.get('min_humidity'),
            max_humidity=body.get('max_humidity'),
            daily_water_freq=body.get('daily_water_freq'),
            water_amount_per_freq=body.get('water_amount_per_freq'),
            timestamp=body.get('timestamp')
        )

        with session_scope() as s:
            s.add(instructions)

        return {"message": "JSON received"}, 200

    return {"error": "Request must be JSON"}, 415


@app.route('/', methods=['GET'])
def hello():
    return "Hello from BBB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
