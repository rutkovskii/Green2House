from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Time
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    datetime_joined = Column(String, nullable=False, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))#.isoformat(' ', 'seconds'))

    def to_dict(self):
        return {
            'phone_number': self.phone_number,
            'email': self.email,
            'datetime_joined': self.datetime_joined
        }

    def __repr__(self):
        return "<User(phone_number='{}',email='{}', datetime_joined='{}')>"\
            .format(self.phone_number, self.email, self.datetime_joined)


class DataSample(Base):
    __tablename__ = 'DataSamples'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False) # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True),nullable=False)
    date = Column(Date, nullable=False) # is it redundant?
    time = Column(Time, nullable=False) # is it redundant?

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'timestamp': self.timestamp,
            'date': self.date,
            'time': self.time
        }

    def __repr__(self):
        return "<DataSample(user_id='{}',temperature='{}', humidity='{}', timestamp='{}', date='{}', time='{}')>"\
            .format(self.user_id, self.temperature, self.humidity, self.timestamp, self.date, self.time)
