from flask import request, Blueprint

get_data_bp = Blueprint('get_data_bp',__name__)


@get_data_bp.route('/get_data')
def get_data():
    json = request.get_json()
