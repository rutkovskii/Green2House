from flask import request, Blueprint, render_template, session
from datetime import datetime as dt
import requests
import json
from flask_login import login_required

env_page_bp = Blueprint('env_page_bp', __name__)

bbb = 'http://172.27.122.183:5000'
url = f'{bbb}/instructions'


@env_page_bp.route('/environment', methods=['GET', 'POST'])
@login_required
def set_environment():
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        times_per_day = request.form['times_per_day']
        timestamp = str(round(dt.timestamp(dt.now())))

        body = json.dumps({'user_id': session['user_id'], 'temperature': temperature,
                          'humidity': humidity, 'times_per_day': times_per_day, 'timestamp': timestamp})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=body, headers=headers)
        print(f"Status Code: {r.status_code}, Response: {r.json()}")

    # generate options for the times per day dropdown
    times_per_day_options = ''
    for i in range(1, 49):
        times_per_day_options += f'<option value="{i}">{i}</option>'

    # render the template with the options for the dropdown
    return render_template('user_env_page.html',
                           times_per_day_options=times_per_day_options,
                           title='Set ENV — Green2House')
