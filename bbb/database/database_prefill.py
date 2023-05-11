from database.models import DataSample
from datetime import datetime as dt
from datetime import date as d
import random


def dt_ts2dt_obj(timestamp):
    """Give datetime object from timestamp"""
    return dt.fromtimestamp(timestamp)


def dt_ts2date(timestamp):
    """Gives date in %y-%m-%d from timestamp"""
    return d.fromtimestamp(timestamp)


def dt_ts2time(timestamp):
    """Gives time in %H:%M:%S from timestamp"""
    return dt.fromtimestamp(timestamp).time()


def dt_obj2date(obj):
    """Gives date in %y-%m-%d from datetime object"""
    return obj.strftime('%y-%m-%d')


def dt_obj2time(obj):
    """Gives time in %H:%M:%S from datetime object"""
    return obj.strftime('%H:%M:%S')


def generate_samples(user_ids, count_per_user):
    samples = []
    for user_id in user_ids:
        for i in range(count_per_user):
            timestamp = int(dt.timestamp(dt.now())) + i*300
            sample = DataSample(
                user_id=user_id,
                temperature=round(random.uniform(75.0, 85.0), 1),
                humidity=round(random.uniform(45.0, 65.0), 1),
                timestamp=dt_ts2dt_obj(timestamp),
                date=dt_ts2date(timestamp),
                time=dt_ts2time(timestamp)
            )
            samples.append(sample)
    return samples


if __name__ == '__main__':
    samples = generate_samples([6, 7], 100)
    print(samples)
