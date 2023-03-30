from flask import request, Blueprint, render_template, session, flash
from flask_login import login_required
from datetime import datetime as dt
from app.database.models import Instructions
from app.database.database import session_scope
from app.user.config import UserConfig

current_env_data_page_bp = Blueprint('current_env_data_page_bp', __name__)


@current_env_data_page_bp.route(UserConfig.CURRENT_ENV_DATA_ROUTE, methods=['GET'])
@login_required
def current_env_data_page():
    """Returns the current environment settings page."""
    with session_scope() as s:
        instructions = s.query(Instructions).filter(
            Instructions.user_id == session['user_id']).order_by(Instructions.id.desc()).first()
        s.expunge(instructions)

        date = instructions.timestamp.strftime('%Y-%m-%d')
        time = instructions.timestamp.strftime('%H:%M:%S')

        # Add date and time to the instructions object as new attributes
        instructions.date = date
        instructions.time = time

    return render_template('/user_current_env_data_page.html', title='Current Environment Data', instructions=instructions)
