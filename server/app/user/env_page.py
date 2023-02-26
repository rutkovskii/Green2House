from flask import request, Blueprint, render_template, session
from flask_login import login_required
from datetime import datetime as dt
import requests
import json


env_page_bp = Blueprint('env_page_bp', __name__)

bbb = 'http://172.27.122.183:5000'
url = f'{bbb}/instructions'


@env_page_bp.route('/environment', methods=['GET', 'POST'])
@login_required
def set_environment():
    if request.method == 'POST':
        body = json.dumps(
            {
                'user_id': session['user_id'],
                'min_temperature': request.form['temperature_min'],
                'max_temperature': request.form['temperature_max'],
                'min_humidity': request.form['humidity_min'],
                'max_humidity': request.form['humidity_max'],
                'daily_water_freq': request.form['daily_water_freq'],
                'water_amount_per_freq': request.form['water_amount_per_freq'],
                'timestamp': str(round(dt.timestamp(dt.now())))
            }
        )
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=body, headers=headers)
        print(f"Status Code: {r.status_code}, Response: {r.json()}")

    # generate options for the times per day dropdown
    daily_water_freq_options = ''
    for i in range(1, 49):
        daily_water_freq_options += f'<option value="{i}">{i}</option>'

    # generate options for the water amount dropdown
    water_amount_per_freq_options = ''
    for j in range(50, 501, 50):
        water_amount_per_freq_options += f'<option value="{j}">{j}</option>'

    # render the template with the options for the dropdown
    return render_template('user_env_page.html',
                           daily_water_freq_options=daily_water_freq_options,
                           water_amount_per_freq_options=water_amount_per_freq_options,
                           title='Set ENV — Green2House')
