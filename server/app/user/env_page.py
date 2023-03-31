from flask import request, Blueprint, render_template, session, flash, jsonify
from flask_login import login_required
from datetime import datetime as dt
import requests
import json
from app.database.models import Instructions
from app.database.database import session_scope
from app.user.config import UserConfig

env_page_bp = Blueprint('env_page_bp', __name__)


@env_page_bp.route(UserConfig.WATER_ROUTE, methods=['GET', 'POST'])
@login_required
def water_plant():
    """Water the plant."""

    if request.method == 'POST':
        data = request.get_json()
        is_pressed = data.get('is_pressed', False)
        print(f'Button is now: {"pressed" if is_pressed else "not pressed"}')

        if is_pressed:
            body = json.dumps(
                {
                    'user_id': session.get('user_id'),
                    'water': True
                }
            )
        else:
            body = json.dumps(
                {
                    'user_id': session.get('user_id'),
                    'water': False
                }
            )

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        try:
            r = requests.post(UserConfig.WATER_URL, json=body, headers=headers)
        except requests.exceptions.ConnectionError as e:
            print(e)
            return jsonify({'success': False})

        print(f"Status Code: {r.status_code}, Response: {r.json()}")

        return jsonify({'success': True})

    return render_template('/water.html', title='Water Plant')


@env_page_bp.route(UserConfig.ENV_ROUTE, methods=['GET', 'POST'])
@login_required
def set_environment():
    if request.method == 'POST':
        # now = round(dt.timestamp(dt.now()))
        now = dt.now()
        body = json.dumps(
            {
                'user_id': session.get('user_id'),
                'min_temperature': request.form.get('temperature_min'),
                'max_temperature': request.form.get('temperature_max'),
                'min_humidity': request.form.get('humidity_min'),
                'max_humidity': request.form.get('humidity_max'),
                'daily_water_freq': request.form.get('daily_water_freq'),
                'water_amount_per_freq': request.form.get('water_amount_per_freq'),
                'timestamp': str(now)  # .isoformat()  # str(now)
            }
        )
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(UserConfig.INSTRUCTIONS_URL,
                          json=body, headers=headers)

        instructions = Instructions(
            user_id=session.get('user_id'),
            min_temperature=request.form.get('temperature_min'),
            max_temperature=request.form.get('temperature_max'),
            min_humidity=request.form.get('humidity_min'),
            max_humidity=request.form.get('humidity_max'),
            daily_water_freq=request.form.get('daily_water_freq'),
            water_amount_per_freq=request.form.get('water_amount_per_freq'),
            timestamp=now  # dt.fromtimestamp(now)
        )

        print(now)

        with session_scope() as s:
            s.add(instructions)

        if r.status_code == 200:
            flash('Environment settings updated successfully', 'success')
        else:
            flash('Environment settings could not be updated', 'danger')

        # print(f"Status Code: {r.status_code}, Response: {r.json()}")

    # generate options for the times per day dropdown
    daily_water_freq_options = ''
    for i in range(1, 49):
        daily_water_freq_options += f'<option value="{i}">{i}</option>'

    # generate options for the water amount dropdown
    water_amount_per_freq_options = ''
    for j in range(10, 501, 10):
        water_amount_per_freq_options += f'<option value="{j}">{j}</option>'

    # render the template with the options for the dropdown
    return render_template('user_env_page.html',
                           daily_water_freq_options=daily_water_freq_options,
                           water_amount_per_freq_options=water_amount_per_freq_options,
                           title='Set ENV — Green2House')
