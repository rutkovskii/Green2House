from flask import request, Blueprint, render_template
from flask_login import login_required

env_page_bp = Blueprint('env_page_bp', __name__)


@env_page_bp.route('/set-environment', methods=['GET', 'POST'])
@login_required
def set_environment():
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        times_per_day = request.form['times_per_day']
        print(temperature, humidity, times_per_day)

        # TODO: send the data to the BBB

    # generate options for the times per day dropdown
    times_per_day_options = ''
    for i in range(1, 49):
        times_per_day_options += f'<option value="{i}">{i}</option>'

    # render the template with the options for the dropdown
    return render_template('user_env_page.html',
                           times_per_day_options=times_per_day_options,
                           title='Set ENV — Green2House')
