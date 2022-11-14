from datetime import datetime as dt


def dt_ts2dt_obj(timestamp):
    """Give datetime object from timestamp"""
    return dt.fromtimestamp(timestamp)

def dt_ts2date(timestamp):
    """Gives date in %d-%m-%y from timestamp"""
    return dt.fromtimestamp(timestamp).strftime('%d-%m-%y')

def dt_ts2time(timestamp):
    """Gives time in %H:%M:%S from timestamp"""
    return dt.fromtimestamp(timestamp).strftime('%H:%M:%S')

def dt_obj2date(obj):
    """Gives date in %d-%m-%y from datetime object"""
    return obj.strftime('%d-%m-%y')

def dt_obj2time(obj):
    """Gives time in %H:%M:%S from datetime object"""
    return obj.strftime('%H:%M:%S')