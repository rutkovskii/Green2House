import os
import time
from math import floor
from datetime import datetime as dt
from bbb_config import BBB_Config as BC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import threading
from database.models import DataSample


def isCommand(file_path):  # detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True


def single_float_pt(number):
    return floor(number * 10) / 10


def getTempHum(sensor):
    sensorF = sensor.temperature * 9 / 5 + 32  # temp in Fahrenheit
    sensorH = sensor.relative_humidity
    return sensorF, sensorH


def getSoilMoisture(pin):  # accepts an ADC pin eg. "AIN0"
    readADC = ADC.read_raw(pin)
    # print(readADC)
    soilPercent = (1 - (readADC - BC.minADC) / (BC.maxADC - BC.minADC))*100
    if readADC >= 2900:  # general soil values
        soil = "dry"
        # relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 2500 <= readADC < 2900:
        soil = "moist"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 1800 < readADC < 2500:
        soil = "wet"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 1450 <= readADC <= 1800:
        soil = "soaked"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    else:
        soil = "Out of Range"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
    return round(soilPercent,1), soil  # give both percent and general reading

def getWaterLevel(pin):  # accepts an ADC pin eg. "AIN0"
    readADC = ADC.read_raw(pin)
    # print(readADC)
    soilPercent = 1 - (readADC - BC.minADC) / (BC.maxADC - BC.minADC)
    if readADC >= 2900:  # general soil values
        soil = "low"
        # relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 2500 <= readADC < 2900:
        soil = "high"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 1800 < readADC < 2500:
        soil = "high"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    elif 1450 <= readADC <= 1800:
        soil = "high"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))

    else:
        soil = "Out of Range"
        # relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
    return soilPercent, soil  # give both percent and general reading


def controlTempHum(sensorF, sensorH):
    # print(int(sensorH))
    # if round(sensorF, 1) <= BC.desiredTemp - BC.tempVariance: #too cold
    if BC.min_temperature and BC.max_temperature:
        ##print("temp: "+str(sensorF))
        #print("\n"+str(BC.max_temperature))
        #print("\n"+str(BC.max_temperature - ((BC.max_temperature - BC.min_temperature)/2)))
        if sensorF <= BC.min_temperature:  # too cold
            close = threading.Thread(target=closeGH)
            close.start()
            relayOn(GPIO, BC.pins_dict.get("heater_relay_pin"))
            BC.heater_status = "on"
            if (int(sensorH) <= BC.max_humidity): 
            # if humidity is low, allow fans to turn off
                relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
                BC.fan_status = "off"

        if sensorF >= BC.min_temperature:
            relayOff(GPIO, BC.pins_dict.get("heater_relay_pin"))
            BC.heater_status = "off"
    

        # elif round(sensorF, 1) <= BC.max_temperature - ((BC.max_temperature - BC.min_temperature)/2):
        #     if int(sensorH) <= BC.max_humidity:
        #         relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
        #         BC.fan_status = "off"

        if sensorF >= BC.max_temperature:
            open = threading.Thread(target=openGH)
            open.start()
            relayOff(GPIO, BC.pins_dict.get("heater_relay_pin"))
            BC.heater_status = "off"
            # Humidity
            relayOn(GPIO, BC.pins_dict.get("fan_relay_pin"))
            BC.fan_status = "on"

        if sensorF <= BC.max_temperature:
            relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
            BC.fan_status = "off"

    if BC.min_humidity and BC.max_humidity:
        # if int(sensorH) > BC.desiredHum:
        if int(sensorH) > BC.max_humidity:
            relayOn(GPIO, BC.pins_dict.get("fan_relay_pin"))
            BC.fan_status = "on"
            relayOff(GPIO, BC.pins_dict.get("mist_relay_pin"))
            BC.mist_status = "off"
            #print("mist sprayer off")

            # turn off water pump only if watering is not happening
            if BC.water_status == "off":
                relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
                BC.pump_status = "off"

        elif int(sensorH) <= BC.min_humidity:
            relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
            relayOn(GPIO, BC.pins_dict.get("mist_relay_pin"))
            time.sleep(1)
            relayOn(GPIO, BC.pins_dict.get("pump_relay_pin"))
            BC.fan_status = "off"
            BC.mist_status = "on"
            BC.pump_status = "on"
            print("mist sprayers on")

        elif BC.min_humidity < int(sensorH) and int(sensorH) < BC.max_humidity:
            relayOff(GPIO, BC.pins_dict.get("mist_relay_pin"))
            BC.mist_status = "off"
            if BC.water_status == "off":
                relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
                BC.pump_status = "off"

        elif int(sensorH) < BC.min_humidity:
            BC.pump_status = "on"
            relayOn(GPIO, BC.pins_dict.get("mist_relay_pin"))
            time.sleep(1)
            relayOn(GPIO, BC.pins_dict.get("pump_relay_pin"))
            BC.mist_status = "on"



def openGH():
    relayOn(GPIO, BC.pins_dict.get("h_bridge1"))
    time.sleep(5)
    relayOff(GPIO, BC.pins_dict.get("h_bridge1"))
    BC.roof_status = "open"

def closeGH():
    relayOn(GPIO, BC.pins_dict.get("h_bridge2"))
    time.sleep(5)
    relayOff(GPIO, BC.pins_dict.get("h_bridge2"))
    BC.roof_status = "closed"

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
    oled.text("Temperature: " + temp + "F", 0, 0, color=1)
    oled.text("Humidity: " + hum + "%", 0, 10, color=1)
    oled.text("Soil is " + moisture, 0, 20, color=1)
    oled.text(timestamp, 0, 30, color=1)
    oled.show()
    return


def sense_sample(user_id, sensorF, sensorH):
    return {
        "user_id": user_id,
        "temperature": single_float_pt(sensorF),
        "humidity": single_float_pt(sensorH),
        # 'soil moisture': #single_float_pt
        "timestamp": int(round(dt.timestamp(dt.now()))),
    }


def sense_sample_db(sensorF, sensorH):
    soil_percent, soil = getSoilMoisture(BC.pins_dict.get("adc_pin"))
    return DataSample(
        user_id=BC.user_id,
        temperature=single_float_pt(sensorF),
        humidity=single_float_pt(sensorH),
        soil_percent=single_float_pt(soil_percent),
    )
