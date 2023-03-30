import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

from bbb_config import BBB_Config as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples_db

from database.database import session_scope

i2c, sensor, oled = create_all(BC.pins_dict)
ADC.setup()


# AIR: 3200
# DRY DIRT: 2900 - 3100
# MOIST DIRT: ~2900
# WET DIRT: 1500
# PURE WATER: 1450


# def measureValues():
#     #soil moisture
#     soilPercent, soil = utils.getSoilMoisture()
#     #DHT20 Temp/Hum
#     sensorF, sensorH = utils.getTempHum(sensor)[0], utils.getTempHum(sensor)[1]
#     values = [soil, sensorF, sensorH]

#     return values


def main():
    # soilPercent is not used but still collected just in case
    soilPercent, soil = utils.getSoilMoisture()
    sensorF, sensorH = utils.getTempHum(sensor)  # measure initial values
    while True:
        if int(time.strftime('%S')) % 2 == 0:  # measure value every x seconds
            # print(measureValues()[0])
            soilPercent, soil = utils.getSoilMoisture()
            sensorF, sensorH = utils.getTempHum(sensor)
            # measurements = measureValues()
            utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum=str(sensorH)[
                           0:4], moisture=soil, timestamp=time.strftime('%H:%M:%S'))

            # Sensing and Adding Sample to database
            sample = utils.sense_sample_db(BC.user_id, sensorF, sensorH)
            with session_scope() as session:
                session.add(sample)

            if BC.SEND_DATA:
                send_samples_db()

            # sleep for at least 1 second to avoid multiple measurements in one second
            time.sleep(1)


if __name__ == "__main__":
    main()
