import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

from bbb_config import BBB_CONFIG as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples

i2c, sensor, oled = create_all(BC.pins_dict)
ADC.setup()


#AIR: 3200
#DRY DIRT: 2900 - 3100
#MOIST DIRT: ~2900
#WET DIRT: 1500
#PURE WATER: 1450


# def measureValues():
#     #soil moisture
#     soilPercent, soil = utils.getSoilMoisture()
#     #DHT20 Temp/Hum
#     sensorF, sensorH = utils.getTempHum(sensor)[0], utils.getTempHum(sensor)[1]
#     values = [soil, sensorF, sensorH]
    
#     return values


def main():
    soilPercent, soil = utils.getSoilMoisture() #soilPercent is not used but still collected just in case
    sensorF, sensorH = utils.getTempHum(sensor) #measure initial values
    while True: 
        if int(time.strftime('%S')) % 2 == 0: # measure value every x seconds
            #print(measureValues()[0])
            soilPercent, soil = utils.getSoilMoisture()
            sensorF, sensorH = utils.getTempHum(sensor)
            #measurements = measureValues()
            utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum=str(sensorH)[0:4], moisture=soil, timestamp=time.strftime('%H:%M:%S'))
            #utils.

            if BC.SEND_DATA:
                sample = utils.sense_sample(BC.user_id, sensorF, sensorH)
                samples = [sample]
                send_samples(url=SERVER_GET_DATA_URL, samples=samples)

            time.sleep(1) #sleep for at least 1 second to avoid multiple measurements in one second

        


if __name__ == "__main__":
    main()