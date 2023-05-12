import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import threading
import multiprocessing
import os

from bbb_config import BBB_Config as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples_db

# from scripts.api import app, latest_instructions

from database.database import session_scope, get_last_instruction

i2c, sensor, oled = create_all(BC.pins_dict)
ADC.setup()


# AIR: 3200
# DRY DIRT: 2900 - 3100
# MOIST DIRT: ~2900
# WET DIRT: 1500
# PURE WATER: 1450


def waterSchedule(hour, min, duratio):
    while True:
        currentTime = time.localtime()
        if currentTime.tm_hour == hour and currentTime.tm_min == min:
            print("water on")
            utils.relayOn(GPIO, BC.pins_dict.get("water_relay_pin"))
            BC.water_status = "on"
            time.sleep(2)
            utils.relayOn(GPIO, BC.pins_dict.get("pump_relay_pin"))
            BC.pump_status = "on"
            time.sleep(duration * 60)

            # turn off pump only if mist sprayers not running
            if BC.mist_status == "off":
                utils.relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
                BC.pump_status = "off"
            utils.relayOff(GPIO, BC.pins_dict.get("water_relay_pin"))
            BC.water_status = "off"
            # turn off water solenoid after pump
            print("water off")
            time.sleep(3600)

        elif currentTime.tm_hour == hour:
            time.sleep(60)  # wait until the next minute to check

        else:
            time.sleep((60 - currentTime.tm_min) * 60)  # sleep for the rest of the hour

        hour = BC.watering_hour
        min = BC.watering_minute
        duration = BC.watering_duration


def main(latest_instructions):
    utils.relayOff(GPIO, BC.pins_dict.get("heater_relay_pin"))
    utils.relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
    utils.relayOff(GPIO, BC.pins_dict.get("water_relay_pin"))
    utils.relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
    utils.relayOff(GPIO, BC.pins_dict.get("mist_relay_pin"))
    close = threading.Thread(target=utils.closeGH)  # close greenhouse upon startup
    close.start()
    close.join()
    BC.heater_status = "off"
    BC.fan_status = "off"
    BC.water_status = "off"
    BC.pump_status = "off"
    BC.mist_status = "off"

    # soilPercent is not used but still collected just in case
    # soilPercent, soil = utils.getSoilMoisture(BC.pins_dict.get('adc_pin'))
    # sensorF, sensorH = utils.getTempHum(sensor)  # measure initial values
    next_time = time.time() + 10
    while True:
        if not latest_instructions.get("shutdown"):
            if time.time() >= next_time + 2:
                # ... take measurements and perform operations ...
                next_time += 10

                # print(measureValues()[0])
                soilPercent, soil = utils.getSoilMoisture(BC.pins_dict.get("adc_pin"))
                tankPercent, tankLevel = utils.getWaterLevel(
                    BC.pins_dict.get("adc2_pin")
                )
                # soilPercent, soil = 50, "dry"
                a, b = utils.getTempHum(sensor)
                sensorF, sensorH = round(a, 2), round(b, 2)
                os.system("clear")
                print("Temperature: " + str(sensorF) + " F")
                print("Humidity: " + str(sensorH) + "%")
                print("Soil moisture: " + str(soilPercent) + "%")
                print("Water level: high")

                # open and write to file as backup for database
                f = open("test_results_5_4.txt", "a")
                f.write(
                    str(time.localtime().tm_mon)
                    + "-"
                    + str(time.localtime().tm_mday)
                    + " "
                    + str(time.strftime("%H:%M:%S"))
                    + ", "
                    + str(sensorF)
                    + ", "
                    + str(sensorH)
                    + "%, soil: "
                    + str(round(soilPercent * 100, 2))
                    + "\n"
                )
                f.close()

                utils.dispOLED(
                    oled=oled,
                    temp=str(sensorF)[0:4],
                    hum=str(sensorH)[0:4],
                    moisture=soil,
                    timestamp=time.strftime("%H:%M:%S"),
                )

                # make appropriate environment changes based on temp and hum
                utils.controlTempHum(sensorF, sensorH)
                print("Heater status: " + BC.heater_status)
                print("Fan status: " + BC.fan_status)
                print("Roof status: " + BC.roof_status)
                print("Pump status: " + BC.pump_status)
                print("Mist sprayer status: " + BC.mist_status)
                print("Soil water status: " + BC.water_status)
                print("Last Measured: " + time.strftime("%H:%M:%S"))
                if BC.watering_minute < 10:
                    print(
                        "Next watering: %s:0%s"
                        % (str(BC.watering_hour), str(int(BC.watering_minute)))
                    )

                else:
                    print(
                        "Next watering: %s:%s"
                        % (str(BC.watering_hour), str(BC.watering_minute))
                    )

                if latest_instructions.get("updated"):
                    if (
                        latest_instructions.get("min_temperature")
                        or latest_instructions.get("max_temperature")
                        or latest_instructions.get("min_humidity")
                        or latest_instructions.get("max_humidity")
                        or latest_instructions.get("watering_time")
                        or latest_instructions.get("watering_duration")
                    ):
                        # Read the latest instructions
                        BC.min_temperature = float(
                            latest_instructions.get("min_temperature")
                        )
                        BC.max_temperature = float(
                            latest_instructions.get("max_temperature")
                        )
                        BC.min_humidity = float(latest_instructions.get("min_humidity"))
                        BC.max_humidity = float(latest_instructions.get("max_humidity"))

                        # watering schedule
                        hour, minute = latest_instructions.get("watering_time").split(
                            ":"
                        )
                        BC.watering_hour = float(hour)
                        BC.watering_minute = float(minute)
                        BC.watering_duration = float(
                            latest_instructions.get("watering_duration")
                        )

                        print("Min Temperature: ", BC.min_temperature)
                        print("Max Temperature: ", BC.max_temperature)
                        print("Min Humidity: ", BC.min_humidity)
                        print("Max Humidity: ", BC.max_humidity)
                        print(
                            "Watering Time: ", BC.watering_hour, ":", BC.watering_minute
                        )
                        print("Watering Duration: ", BC.watering_duration)

                        latest_instructions["updated"] = False

                # Sensing and Adding Sample to database
                sample = utils.sense_sample_db(sensorF, sensorH)
                with session_scope() as session:
                    session.add(sample)

                if BC.SEND_DATA:
                    print("Sending")
                    send_samples_db()
                    print("Sent")

                # sleep for at least 1 second to avoid multiple measurements in one second
                time.sleep(1)

        elif latest_instructions.get("shutdown"):
            if latest_instructions.get("water"):
                print("Watering plant")
                utils.relayOn(GPIO, BC.pins_dict.get("water_relay_pin"))
                time.sleep(1)
                utils.relayOn(GPIO, BC.pins_dict.get("pump_relay_pin"))
                time.sleep(10)  # Keep the relay on for 5 seconds
                utils.relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
                utils.relayOff(GPIO, BC.pins_dict.get("water_relay_pin"))
                latest_instructions["water"] = False

            elif latest_instructions.get("mist"):
                print("Activating misters")
                utils.relayOn(GPIO, BC.pins_dict.get("mist_relay_pin"))
                time.sleep(1)
                utils.relayOn(GPIO, BC.pins_Dict.get("pump_relay_pin"))
                time.sleep(10)
                utils.relayOff(GPIO, BC.pins_dict.get("pump_relay_pin"))
                utils.relayOff(GPIO, BC.pins_dict.get("mist_relay_pin"))
                latest_instructions["mist"] = False

            elif latest_instructions.get("lid"):
                print("Opening roof")
                open_greenhouse = threading.Thread(
                    target=utils.openGH
                )  # close greenhouse upon startup
                open_greenhouse.start()
                open_greenhouse.join()
                time.sleep(5)
                print("Closing roof")
                close = threading.Thread(
                    target=utils.closeGH
                )  # close greenhouse upon startup
                close.start()
                close.join()
                latest_instructions["lid"] = False

            elif latest_instructions.get("fan"):
                print("Activating fan")
                utils.relayOn(GPIO, BC.pins_dict.get("fan_relay_pin"))
                time.sleep(10)
                utils.relayOff(GPIO, BC.pins_dict.get("fan_relay_pin"))
                latest_instructions["fan"] = False

            elif latest_instructions.get("heat"):
                print("Activating heater")
                utils.relayOn(GPIO, BC.pins_dict.get("heater_relay_pin"))
                time.sleep(10)
                utils.relayOff(GPIO, BC.pins_dict.get("heater_relay_pin"))
                latest_instructions["heat"] = False

            latest_instructions["shutdown"] = False


if __name__ == "__main__":
    # Run main in a separate thread
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # Set up the two processes
    flask_process = multiprocessing.Process(
        target=app.run, kwargs={"host": "0.0.0.0", "port": 5000, "debug": False}
    )
    schedule_process = multiprocessing.Process(
        target=waterSchedule,
        args=(BC.watering_hour, BC.watering_minute, BC.watering_duration),
    )

    # Start the processes
    flask_process.start()
    schedule_process.start()

    # Wait for the thread and processes to finish
    main_thread.join()
    flask_process.join()
    schedule_process.join()

