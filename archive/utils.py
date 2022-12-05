import os
from math import floor
from datetime import datetime as dt


def isCommand(file_path): #detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True


def single_float_pt(number):
    return floor(number*10)/10


def getTempHum(sensor):
    sensorF = sensor.temperature*9/5 + 32 #temp in Fahrenheit
    sensorH = sensor.relative_humidity
    return sensorF, sensorH


def relayOn(GPIO, pin):
    GPIO.output(pin, GPIO.HIGH)
    return


def relayOff(GPIO, pin):
    GPIO.output(pin, GPIO.LOW)
    return


def dispOLED(oled, temp, hum, timestamp):
    oled.fill(0)
    oled.text("Temperature: "+temp+"F", 0, 0, color=1)
    oled.text("Humidity: "+hum+"%", 0, 10, color=1)
    oled.text(timestamp, 0, 20, color=1)
    oled.show()
    return


def sense_sample(user_id,sensorF,sensorH):
    return {'user_id': user_id,
              'temperature': single_float_pt(sensorF),
              'humidity': single_float_pt(sensorH),
              'timestamp': int(round(dt.timestamp(dt.now())))
              }