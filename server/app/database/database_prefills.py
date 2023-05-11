from app.database.models import User, DataSample
import app.utils as u

tm1 = 1667351400
tm2 = 1667279700
tm3 = 1667279500
tm4 = 1667279800

prefill_users = [
    User(name='Mike Green', phone_number='+55555',
         email='mike@umass.edu', auth_token='12345'),
    User(name='Rob Green', phone_number='+44444',
         email='rob@umass.edu', auth_token='12345'),
    User(name='John Green', phone_number='+33333',
         email='john@umass.edu', auth_token='12345'),
    User(name='Cole Green', phone_number='+33333',
         email='cole@umass.edu', auth_token='12345'),
]


prefill_samples = [
    DataSample(user_id=6, temperature=78.3, humidity=43.2, timestamp=u.dt_ts2dt_obj(tm1),
               date=u.dt_ts2date(tm1), time=u.dt_ts2time(tm1)
               ),
    DataSample(user_id=6, temperature=78.7, humidity=61.5, timestamp=u.dt_ts2dt_obj(tm2),
               date=u.dt_ts2date(tm2), time=u.dt_ts2time(tm2)
               ),
    DataSample(user_id=6, temperature=81.3, humidity=61.9, timestamp=u.dt_ts2dt_obj(tm3),
               date=u.dt_ts2date(tm3), time=u.dt_ts2time(tm3)
               ),
    DataSample(user_id=6, temperature=81.7, humidity=40.9, timestamp=u.dt_ts2dt_obj(tm4),
               date=u.dt_ts2date(tm4), time=u.dt_ts2time(tm4)
               ),
    DataSample(user_id=7, temperature=78.3, humidity=43.2, timestamp=u.dt_ts2dt_obj(tm1),
               date=u.dt_ts2date(tm1), time=u.dt_ts2time(tm1)
               ),
    DataSample(user_id=7, temperature=78.7, humidity=61.5, timestamp=u.dt_ts2dt_obj(tm2),
               date=u.dt_ts2date(tm2), time=u.dt_ts2time(tm2)
               ),
    DataSample(user_id=7, temperature=81.3, humidity=61.9, timestamp=u.dt_ts2dt_obj(tm3),
               date=u.dt_ts2date(tm3), time=u.dt_ts2time(tm3)
               ),
    DataSample(user_id=7, temperature=81.7, humidity=40.9, timestamp=u.dt_ts2dt_obj(tm4),
               date=u.dt_ts2date(tm4), time=u.dt_ts2time(tm4)
               )
]
