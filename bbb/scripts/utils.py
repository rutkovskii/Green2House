import os
import time
from math import floor
from datetime import datetime as dt
from bbb_config import BBB_Config as BC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

from database.models import DataSample


def isCommand(file_path):  # detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True


def single_float_pt(number):
    return floor(number*10)/10


def getTempHum(sensor):
    sensorF = sensor.temperature*9/5 + 32  # temp in Fahrenheit
    sensorH = sensor.relative_humidity
    return sensorF, sensorH


def getSoilMoisture(pin): #accepts an ADC pin eg. "AIN0"
    readADC = ADC.read_raw(pin)
    #print(readADC)
    soilPercent = 1 - (readADC - BC.minADC) / (BC.maxADC - BC.minADC)
    print("Soil moisture: " + str(round(soilPercent*100,2)) + "%") #print % moisture to console window
    if readADC >= 2900: #general soil values
        soil = "dry"
        relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 2500 <= readADC < 2900:
        soil = "moist"
        relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))


    elif 1800 < readADC < 2500:
        soil = "wet"
        relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
    
    elif 1450 <= readADC <= 1800:
        soil = "soaked"
        relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    else:
        soil = "Out of Range"
        relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
    return soilPercent, soil #give both percent and general reading


def controlTempHum(sensorF, sensorH):
    #print(int(sensorH))
    if round(sensorF, 1) <= BC.desiredTemp - BC.tempVariance: #too cold
        closeGH()
        relayOn(GPIO, BC.pins_dict.get('heater_relay_pin'))
        if int(sensorH) <= BC.desiredHum: #if humidity is low, allow fans to turn off
            relayOff(GPIO, BC.pins_dict.get('fan_relay_pin'))
    
    elif round(sensorF, 1) >= BC.desiredTemp + BC.tempVariance: #too hot
        openGH()
        relayOff(GPIO, BC.pins_dict.get('heater_relay_pin'))
        #Humidity 
        relayOn(GPIO, BC.pins_dict.get('fan_relay_pin'))

    if int(sensorH) > BC.desiredHum:
        relayOn(GPIO, BC.pins_dict.get('fan_relay_pin'))
    
    elif int(sensorH) <= BC.desiredHum and round(sensorF, 2) <= BC.desiredTemp - BC.tempVariance:
        relayOff(GPIO, BC.pins_dict.get('fan_relay_pin'))


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


def sense_sample(user_id, sensorF, sensorH):
    return {'user_id': user_id,
            'temperature': single_float_pt(sensorF),
            'humidity': single_float_pt(sensorH),
            # 'soil moisture': #single_float_pt
            'timestamp': int(round(dt.timestamp(dt.now())))
            }


def sense_sample_db(sensorF, sensorH):
    soil_percent, soil = getSoilMoisture(BC.pins_dict.get('adc_pin'))
    return DataSample(user_id=BC.user_id,
                      temperature=single_float_pt(sensorF),
                      humidity=single_float_pt(sensorH),
                      soil_percent=single_float_pt(soil_percent),
                      )
