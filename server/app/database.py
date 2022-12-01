import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
# When running run.py
from app.models import Base, User, DataSample
from app.admin.config import DATABASE_URI
import app.utils as u

# When running database.py
# from models import Base, User, DataSample
# from admin.config import DATABASE_URI
# import utils as u



engine = sqlalchemy.create_engine(DATABASE_URI)  #Server -> necessary for cron
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

#print(engine)

tm1=1667351400
tm2=1667279700
tm3=1667279500
tm4=1667279800


def add_sample_users():
    s = Session()
    bulk_list = [
        User(phone_number='+55555',email='arutkovskii@umass.edu'),
        User(phone_number='+11111',email='smorelli@umass.edu')
    ]
    s.bulk_save_objects(bulk_list)
    s.commit()
    s.close()



def add_example_datasamples():
    s = Session()
    bulk_list = [
        DataSample(user_id=1,temperature=78.3, humidity=43.2, timestamp=u.dt_ts2dt_obj(tm1),
                   date=u.dt_ts2date(tm1),time=u.dt_ts2time(tm1)
                   ),
        DataSample(user_id=1, temperature=78.7, humidity=61.5, timestamp=u.dt_ts2dt_obj(tm2),
                   date=u.dt_ts2date(tm2), time=u.dt_ts2time(tm2)
                   ),
        DataSample(user_id=2, temperature=81.3, humidity=61.9, timestamp=u.dt_ts2dt_obj(tm3),
                   date=u.dt_ts2date(tm3), time=u.dt_ts2time(tm3)
                   ),
        DataSample(user_id=2, temperature=81.7, humidity=40.9, timestamp=u.dt_ts2dt_obj(tm4),
                   date=u.dt_ts2date(tm4), time=u.dt_ts2time(tm4)
                   )
    ]
    s.bulk_save_objects(bulk_list)
    s.commit()
    s.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


#    with session_scope() as s:
        #s.add(book)


if __name__ == "__main__":
    # When running database.py
    # recreate_database()
    # add_sample_users()
    # add_example_datasamples()

    pass