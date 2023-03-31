import board
import adafruit_ahtx0
import adafruit_ssd1306
# import Adafruit_SSD1306 as adafruit_ssd1306
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC


def init_i2c():
    return board.I2C()  # uses board.SCL and board.SDA


def init_sensor(i2c):
    # Create sensor object, communicating over the board's default I2C bus
    return adafruit_ahtx0.AHTx0(i2c)


def init_oled(i2c):
    return adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


def set_up_pins(pins_dict):
    # Pump Relay
    if pins_dict['pump_relay_pin']:
        GPIO.setup(pins_dict['pump_relay_pin'], GPIO.OUT)
    else:
        print("pump_relay_pin is None")

    # Temperature Relay
    if pins_dict['fan_relay_pin']:
        GPIO.setup(pins_dict['fan_relay_pin'], GPIO.OUT)
    else:
        print("fan_relay_pin is None")

    # Button pin
    if pins_dict['heater_relay_pin']:
        GPIO.setup(pins_dict['heater_relay_pin'], GPIO.OUT)
    else:
        print("heater_relay_pin is None")

    if pins_dict['h_bridge1']:
        GPIO.setup(pins_dict['h_bridge1'], GPIO.OUT)

    else:
        print('h_bridge1 is None')

    if pins_dict['h_bridge2']:
        GPIO.setup(pins_dict['h_bridge2'], GPIO.OUT)

    else:
        print('h_bridge2 is None')

    if pins_dict['button_pin']:
        GPIO.setup(pins_dict['button_pin'], GPIO.IN)

    else:
        print('button_pin is None')


def create_all(pins_dict):
    set_up_pins(pins_dict)

    i2c = init_i2c()
    sensor = init_sensor(i2c)
    oled = init_oled(i2c)
    ADC.setup()

    return i2c, sensor, oled

# import board
# import adafruit_ahtx0
# import adafruit_ssd1306
# import Adafruit_BBIO.GPIO as GPIO
# import Adafruit_BBIO.ADC as ADC


# def init_i2c():
#     return board.I2C()  # uses board.SCL and board.SDA


# def init_sensor(i2c):
#     # Create sensor object, communicating over the board's default I2C bus
#     return adafruit_ahtx0.AHTx0(i2c)


# def init_oled(i2c):
#     return adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


# def set_up_pins(pins_dict):
#     # Pump Relay
#     if pins_dict['pump_relay_pin']:
#         GPIO.setup(pins_dict['pump_relay_pin'], GPIO.OUT)
#     else:
#         print("pump_relay_pin is None")

#     # Temperature Relay
#     if pins_dict['fan_relay_pin']:
#         GPIO.setup(pins_dict['fan_relay_pin'], GPIO.OUT)
#     else:
#         print("fan_relay_pin is None")

#     # Button pin
#     if pins_dict['heater_relay_pin']:
#         GPIO.setup(pins_dict['heater_relay_pin'], GPIO.OUT)
#     else:
#         print("heater_relay_pin is None")


# def create_all(pins_dict):
#     set_up_pins(pins_dict)

#     i2c = init_i2c()
#     sensor = init_sensor(i2c)
#     oled = init_oled(i2c)
#     ADC.setup()

#     return i2c, sensor, oled
