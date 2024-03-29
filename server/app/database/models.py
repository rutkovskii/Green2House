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
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "datetime_joined": self.datetime_joined,
        }

    def __repr__(self):
        return "<User(id='{}',<User(name='{}', phone_number='{}', email='{}', datetime_joined='{}')>".format(
            self.id, self.name, self.phone_number, self.email, self.datetime_joined
        )


class DataSample(Base):
    __tablename__ = "DataSamples"
    id = Column(Integer, primary_key=True)
    # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    user_id = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    soil_percent = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    date_time = Column(String, nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "soil_percent": self.soil_percent,
            "timestamp": self.timestamp,
            "date": self.date,
            "time": self.time,
            "date_time": self.date_time,
        }

    def to_dict_charts(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "soil_percent": self.soil_percent,
            "date": self.date.isoformat(),
            "time": self.time.strftime("%H:%M:%S"),
            "date_time": self.date_time,
        }

    def __repr__(self):
        return "<DataSample(user_id='{}', temperature='{}', humidity='{}', soil_percent='{}', timestamp='{}', date='{}', time='{}', date_time='{}')>".format(
            self.user_id,
            self.temperature,
            self.humidity,
            self.soil_percent,
            self.timestamp,
            self.date,
            self.time,
            self.date_time,
        )


class Instructions(Base):
    __tablename__ = "Instructions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)
    watering_time = Column(String, nullable=False)
    watering_duration = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "min_temperature": self.min_temperature,
            "max_temperature": self.max_temperature,
            "min_humidity": self.min_humidity,
            "max_humidity": self.max_humidity,
            "watering_time": self.watering_time,
            "watering_duration": self.watering_duration,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return "<Instructions(user_id='{}', min_temperature='{}', max_temperature='{}', min_humidity='{}', max_humidity='{}', watering_time='{}', watering_duration='{}', timestamp='{}')>".format(
            self.user_id,
            self.min_temperature,
            self.max_temperature,
            self.min_humidity,
            self.max_humidity,
            self.watering_time,
            self.watering_duration,
            self.timestamp,
        )
