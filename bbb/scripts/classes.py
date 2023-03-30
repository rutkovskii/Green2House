import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO


class Sensor:
    def __init__(self, type, pin=None, direction=None):
        self.pin = pin
        self.direction = direction
        self.type = type


class soilMoisture:
    def __init__(self, pin):
        self.pin = pin
        ADC.setup()

    def readMoisture(self):
        print(ADC.read(self.pin))
