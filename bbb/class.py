import Adafruit_BBIO.GPIO as GPIO

class device:
    def __init__(self, pin, direction):
        self.pin = pin
        self.direction = direction
