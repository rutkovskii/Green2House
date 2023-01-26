from flask import Blueprint, render_template
from flask_login import login_required

home_page_bp = Blueprint('home_bp', __name__)


@login_required
@home_page_bp.route('/home')
def home():
    return render_template('/user_home_page.html', title='Home — Green2House')