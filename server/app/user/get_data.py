from flask import request, Blueprint
from flask_login import login_required
import json
from datetime import datetime

from app.database.database import session_scope
from app.database.models import DataSample
from app.admin.config import AdminConfig
import app.utils as u


get_data_bp = Blueprint("get_data_bp", __name__)


@get_data_bp.route(AdminConfig.GET_DATA_ROUTE, methods=["POST"])
# @login_required
def get_data():
    if request.is_json:
        bulk_list = []
        for sample in json.loads(request.get_json()):
            print(sample)

            timestamp_str = sample.get("timestamp")
            timestamp_format = "%Y-%m-%d %H:%M:%S"
            timestamp_dt = datetime.strptime(timestamp_str, timestamp_format)

            # Convert the datetime object to a Unix timestamp (integer)
            timestamp_unix = int(timestamp_dt.timestamp()) - 14400

            # for sample in request.get_json():
            bulk_list.append(
                DataSample(
                    user_id=int(sample.get("user_id")),
                    temperature=sample.get("temperature"),
                    humidity=sample.get("humidity"),
                    timestamp=u.dt_ts2dt_obj(timestamp_unix),
                    date=u.dt_ts2date(timestamp_unix),
                    time=u.dt_ts2time(timestamp_unix),
                )
            )

        with session_scope() as s:
            s.bulk_save_objects(bulk_list)

        return {"message": "JSON received"}, 200

    return {"error": "Request must be JSON"}, 415
