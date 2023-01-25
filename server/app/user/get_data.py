from flask import request, Blueprint
import json

from app.database import Session
from app.models import DataSample
from app.admin.config import SERVER_CONFIG
import app.utils as u


get_data_bp = Blueprint('get_data_bp', __name__)


@get_data_bp.route(SERVER_CONFIG.GET_DATA_ROUTE, methods=['POST'])
def get_data():
    if request.is_json:

        bulk_list = []
        for sample in json.loads(request.get_json()):
            bulk_list.append(
                DataSample(
                    user_id=sample['user_id'],
                    temperature=sample['temperature'],
                    humidity=sample['humidity'],
                    timestamp=u.dt_ts2dt_obj(sample['timestamp']),
                    date=u.dt_ts2date(sample['timestamp']),
                    time=u.dt_ts2time(sample['timestamp'])
                )
            )

        s = Session()
        s.bulk_save_objects(bulk_list)
        s.commit()
        s.close()

        return {"message": "JSON received"}, 200

    return {"error": "Request must be JSON"}, 415
