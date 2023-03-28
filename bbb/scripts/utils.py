import os
from math import floor
from datetime import datetime as dt
from bbb_config import BBB_CONFIG as BC
import Adafruit_BBIO.GPIO as GPIO
import time


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

def getSoilMoisture(pin): #accepts an ADC pin eg. "AIN0"
    readADC = ADC.read_raw(pin)
    soilPercent = 1 - (readADC - BC.minADC) / (BC.maxADC - BC.minADC)
    print("Soil moisture: " + str(round(soilPercent*100,2)) + "%") #print % moisture to console window
    if readADC >= 2900: #general soil values
        soil = "dry"

    elif 2500 <= readADC < 2900:
        soil = "moist"

    elif 1800 < readADC < 2500:
        soil = "wet"
    
    elif 1450 <= readADC <= 1800:
        soil = "soaked"

    else:
        soil = "Out of Range"
    return soilPercent, soil #give both percent and general reading

def controlTemp(sensorF):
    if int(sensorF) <= BC.threshold - BC.variance: #too cold
        relayOn(GPIO, BC.pins_dict.get('heater_relay_pin'))
        relayOff(GPIO, BC.pins_dict.get('fan_relay_pin'))
    
    elif int(sensorF) >= BC.threshold + BC.variance: #too hot
        relayOff(GPIO, BC.pins_dict.get('heater_relay_pin'))
        relayOn(GPIO, BC.pins_dict.get('fan_relay_pin'))

def openGH():
    relayOn(GPIO, BC.pins_dict.get('h_bridge1'))
    time.sleep(3)
    relayOff(GPIO, BC.pins_dict.get('h_bridge1'))

def closeGH():
    relayOn(GPIO, BC.pins_dict.get('h_bridge2'))
    time.sleep(3)
    relayOff(GPIO, BC.pins_dict.get('h_bridge2'))

def relayOn(GPIO, pin):
    GPIO.output(pin, GPIO.HIGH)
    return


def relayOff(GPIO, pin):
    GPIO.output(pin, GPIO.LOW)
    return


def pumpOn(GPIO, pin):
    return GPIO.input(pin)


def dispOLED(oled, temp, hum, moisture, timestamp):
    oled.fill(0)
    oled.text("Temperature: "+temp+"F", 0, 0, color=1)
    oled.text("Humidity: "+hum+"%", 0, 10, color=1)
    oled.text("Soil is "+moisture, 0, 20, color=1)
    oled.text(timestamp, 0, 30, color=1)
    oled.show()
    return


def sense_sample(user_id,sensorF,sensorH):
    return {'user_id': user_id,
              'temperature': single_float_pt(sensorF),
              'humidity': single_float_pt(sensorH),
              #'soil moisture': #single_float_pt
              'timestamp': int(round(dt.timestamp(dt.now())))
              }