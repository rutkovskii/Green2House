from flask import Flask, request, jsonify
from database.models import Instructions
from database.database import session_scope
from datetime import datetime
import json


app = Flask(__name__)

latest_instructions = {
    'water': False,
    'min_temperature': None,
    'max_temperature': None,
    'min_humidity': None,
    'max_humidity': None,
    'daily_water_freq': None,
    'water_amount_per_freq': None,
    'timestamp': None,
    'updated': False
}


@app.route('/water-plant', methods=['POST'])
def water_plant():
    if request.method == 'POST':
        body = json.loads(request.get_json())

        global latest_instructions
        latest_instructions['water'] = body['water']

        print(body)

        return jsonify({'message': 'OK'})

    return jsonify({'error': 'Request must be JSON'})


@app.route('/instructions', methods=['POST'])
def instructions():
    if request.method == 'POST':
        data = json.loads(request.get_json())
        print(data)
        date_string = data['timestamp']
        date_format = "%Y-%m-%d %H:%M:%S.%f"

        datetime_object = datetime.strptime(date_string, date_format)
        timestamp = datetime_object.timestamp()

        data['timestamp'] = datetime.fromtimestamp(timestamp)

        print(data)

        latest_instructions['min_temperature'] = data['min_temperature']
        latest_instructions['max_temperature'] = data['max_temperature']
        latest_instructions['min_humidity'] = data['min_humidity']
        latest_instructions['max_humidity'] = data['max_humidity']

        latest_instructions['updated'] = True

        instructions = Instructions(
            user_id=data.get('user_id'),
            min_temperature=data.get('min_temperature'),
            max_temperature=data.get('max_temperature'),
            min_humidity=data.get('min_humidity'),
            max_humidity=data.get('max_humidity'),
            daily_water_freq=data.get('daily_water_freq'),
            water_amount_per_freq=data.get('water_amount_per_freq'),
            timestamp=data.get('timestamp')
        )

        with session_scope() as s:
            s.add(instructions)

        return jsonify({'message': 'OK'})

    return jsonify({'error': 'Request must be JSON'})


@ app.route('/', methods=['GET'])
def hello():
    return "Hello from BBB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
