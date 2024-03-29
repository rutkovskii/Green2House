from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    DateTime,
    Date,
    Time,
    func,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz


Base = declarative_base()


class DataSample(Base):
    __tablename__ = "DataSamples"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    soil_percent = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    date = Column(
        Date, nullable=False, default=datetime.now(pytz.timezone("US/Eastern")).date
    )
    time = Column(
        Time, nullable=False, default=datetime.now(pytz.timezone("US/Eastern")).time
    )
    sent = Column(Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "soil_percent": self.soil_percent,
            "timestamp": str(self.timestamp),
            "date": str(self.date),
            "time": str(self.time),
        }

    def __repr__(self):
        return "<DataSample(user_id='{}',temperature='{}', humidity='{}', soil_percent='{}', timestamp='{}', date='{}', time='{}', sent='{}')>".format(
            self.user_id,
            self.temperature,
            self.humidity,
            self.soil_percent,
            self.timestamp,
            self.date,
            self.time,
            self.sent,
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
    timestamp = Column(Integer, nullable=False)

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
