from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Time, Boolean
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String(150))
    is_admin = Column(Boolean, nullable=False, default=False)
    auth_token = Column(String, nullable=False)
    datetime_joined = Column(
        String, nullable=False, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )  # .isoformat(' ', 'seconds'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_token(self, token):
        return self.auth_token == token

    def get_auth_token(self):
        return self.auth_token

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    def get_is_admin(self):
        return self.is_admin

    def to_dict(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "datetime_joined": self.datetime_joined,
        }

    def __repr__(self):
        return "<User(name='{}', phone_number='{}', email='{}', datetime_joined='{}')>".format(
            self.name, self.phone_number, self.email, self.datetime_joined
        )


class DataSample(Base):
    __tablename__ = "DataSamples"
    id = Column(Integer, primary_key=True)
    # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    user_id = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    date = Column(Date, nullable=False)  # is it redundant?
    time = Column(Time, nullable=False)  # is it redundant?

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp,
            "date": self.date,
            "time": self.time,
        }

    def __repr__(self):
        return "<DataSample(user_id='{}',temperature='{}', humidity='{}', timestamp='{}', date='{}', time='{}')>".format(
            self.user_id,
            self.temperature,
            self.humidity,
            self.timestamp,
            self.date,
            self.time,
        )


class Instructions(Base):
    __tablename__ = "Instructions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)
    watering_time = Column(Integer, nullable=False)
    watering_amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "min_temperature": self.min_temperature,
            "max_temperature": self.max_temperature,
            "min_humidity": self.min_humidity,
            "max_humidity": self.max_humidity,
            "watering_time": self.watering_time,
            "watering_amount": self.watering_amount,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return "<Instructions(user_id='{}', min_temperature='{}', max_temperature='{}', min_humidity='{}', max_humidity='{}', watering_time='{}', watering_amount='{}', timestamp='{}')>".format(
            self.user_id,
            self.min_temperature,
            self.max_temperature,
            self.min_humidity,
            self.max_humidity,
            self.watering_time,
            self.watering_amount,
            self.timestamp,
        )
