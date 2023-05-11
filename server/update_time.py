from datetime import timedelta

from app.database.database import session_scope
from app.database.models import DataSample
from app.server_logger import setup_logger, log_errors

logger = setup_logger(__name__, "database.log")


@log_errors(logger)
def update_time_datasamples():
    with session_scope() as s:
        data_samples = s.query(DataSample).all()
        time_to_add = timedelta(seconds=14400)

        for data_sample in data_samples:
            data_sample.timestamp += time_to_add
            data_sample.date = data_sample.timestamp.date()
            data_sample.time = data_sample.timestamp.time()


if __name__ == "__main__":
    update_time_datasamples()
