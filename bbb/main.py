import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

from bbb_config import BBB_Config as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples_db

from scripts.api import app, latest_instructions

from database.database import session_scope, get_last_instruction

i2c, sensor, oled = create_all(BC.pins_dict)
ADC.setup()


# AIR: 3200
# DRY DIRT: 2900 - 3100
# MOIST DIRT: ~2900
# WET DIRT: 1500
# PURE WATER: 1450


def waterSchedule(hour, min, duration):
    while True:
        currentTime = time.localtime()
        if currentTime.tm_hour == hour and currentTime.tm_min == min:
            print("water on")
            utils.relayOn(GPIO, BC.pins_dict.get('water_relay_pin'))
            time.sleep(2)
            utils.relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))
            time.sleep(duration*60)

            #turn off pump only if mist sprayers not running
            if GPIO.output(BC.pins_dict.get('mist_relay_pin')) == GPIO.LOW:
                utils.relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
            utils.relayOff(GPIO, BC.pins_dict.get('water_relay_pin'))
            #turn off water solenoid after pump
            print("water off")
            time.sleep(3600)

        elif currentTime.tm_hour == hour:
            time.sleep(60) #wait until the next minute to check
            
        else:
            time.sleep( (60 - currentTime.tm_min) * 60) #sleep for the rest of the hour
        
        hour = BC.waterHour
        min = BC.waterMin
        duration = BC.waterDuration

def main():
    utils.relayOff(GPIO, BC.pins_dict.get('heater_relay_pin'))
    utils.relayOff(GPIO, BC.pins_dict.get('fan_relay_pin'))
    utils.relayOff(GPIO, BC.pins_dict.get('water_relay_pin'))
    utils.relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
    utils.relayOff(GPIO, BC.pins_dict.get('mist_relay_pin'))
    
    # soilPercent is not used but still collected just in case
    # soilPercent, soil = utils.getSoilMoisture(BC.pins_dict.get('adc_pin'))
    # sensorF, sensorH = utils.getTempHum(sensor)  # measure initial values
    while True:
        if int(time.strftime('%S')) % 5 == 0:  # measure value every x seconds
            # print(measureValues()[0])
            soilPercent, soil = utils.getSoilMoisture(BC.pins_dict.get('adc_pin'))
            sensorF, sensorH = utils.getTempHum(sensor)
            time.sleep(1)
            # measurements = measureValues()
            utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum=str(sensorH)[0:4], moisture=soil, timestamp=time.strftime('%H:%M:%S'))

            # make appropriate environment changes based on temp and hum
            utils.controlTempHum(sensorF, sensorH)

            print(latest_instructions.get('water'))
            if latest_instructions.get('water'):
                print("Watering plant")
                utils.relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))
                time.sleep(10)  # Keep the relay on for 5 seconds
                utils.relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
                latest_instructions['water'] = False

            if latest_instructions.get('updated'):
                if latest_instructions.get('min_temperature') or latest_instructions.get('max_temperature') or latest_instructions.get('min_humidity') or latest_instructions.get('max_humidity'):
                    # Read the latest instructions
                    BC.min_temperature = float(latest_instructions.get('min_temperature'))
                    BC.max_temperature = float(latest_instructions.get('max_temperature'))
                    BC.min_humidity = float(latest_instructions.get('min_humidity'))
                    BC.max_humidity = float(latest_instructions.get('max_humidity'))

                    #to be added
                    #BC.scheduleHour = float(latest_instructions.get('waterHour')
                    #BC.scheduleMin = float(latest_instructions.get('waterMin')
                    #BC.scheduleDuration = float(latest_instructions.get('waterDuration')

                    print("Min Temperature: ", BC.min_temperature)
                    print("Max Temperature: ", BC.max_temperature)
                    print("Min Humidity: ", BC.min_humidity)
                    print("Max Humidity: ", BC.max_humidity)

                    latest_instructions['updated'] = False
                
            # Sensing and Adding Sample to database
            sample = utils.sense_sample_db(sensorF, sensorH)
            with session_scope() as session:
                session.add(sample)

            if BC.SEND_DATA:
                send_samples_db()

            # sleep for at least 1 second to avoid multiple measurements in one second
            time.sleep(1)


if __name__ == "__main__":
    print("Time: "+str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min))
    print("Time of next watering: "+str(BC.waterHour)+":"+str(BC.waterMin))

    import threading
    print("starting")
    main_thread = threading.Thread(target=main)
    main_thread.start()
    print("main thread started")
    #connect code here
    scheduleThread = threading.Thread(target=waterSchedule, args=(BC.waterHour, BC.waterMin, BC.waterDuration))
    scheduleThread.start()
    print("schedule thread started")

    app.run(host='0.0.0.0', port=5000, debug=True)
