import board
import adafruit_ahtx0, adafruit_ssd1306
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
# import busio as io


def init_i2c():
    return board.I2C()  # uses board.SCL and board.SDA


def init_sensor(i2c):
    # Create sensor object, communicating over the board's default I2C bus
    return adafruit_ahtx0.AHTx0(i2c)


def init_oled(i2c):
    return adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


def create_all():
    GPIO.setup("P9_15", GPIO.OUT)

    i2c = init_i2c()
    sensor = init_sensor(i2c)
    oled = init_oled(i2c)
    ADC.setup()

    return i2c, sensor, oled