from datetime import datetime as dt
from datetime import date as d


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
    return obj.strftime("%y-%m-%d")


def dt_obj2time(obj):
    """Gives time in %H:%M:%S from datetime object"""
    return obj.strftime("%H:%M:%S")


def class_to_dict(cls):
    return {
        key: value for key, value in cls.__dict__.items() if not key.startswith("__")
    }
