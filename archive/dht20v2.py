import time
import Adafruit_BBIO.GPIO as GPIO

from bbb_config import BBB_CONFIG as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils

i2c, sensor, oled = create_all(BC.pins_dict)


#############################
# Created utils.py — with sensing functions
# Created init_home.py — to initialize the sensor, OLED, i2c, and do set up of GPIO and ADC
# Modified sensing functions a bit to make them more modular
# Created sense_sample() to create a sample
# Modifed send_sample_data() to send_samples()

# Created bbb_config.py
# organized the file structure

#############################


def console(): #process user command
    # file = "data.csv"
    # csv_file = open(file, 'a')
    # csv_write = csv.writer(csv_file)
    # csv_write.writerow(dataRow)

    if int(time.strftime('%S')) % 10 == 0: # sense data every 10 seconds
        sensorF = utils.getTempHum(sensor)[0]
        sensorH = utils.getTempHum(sensor)[1]
        #print(time.strftime('%S'))
        print("Temperature: %2.1f°F\nHumidity: %2.0f%%" %(sensorF, sensorH))

        # Create Sample to propagate to the database
        # sample = sense_sample(BC.user_id,sensorF,sensorH)
        # samples = [sample]

        utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum=str(sensorH)[0:4], timestamp=time.strftime('%H:%M:%S'))
        time.sleep(8)

        # temp_string = str(round(sensorF, 1))
        # hum_string = str(sensorH)
        # dataRow = [time.strftime('%m/%d/%Y %H:%M:%S'), temp_string[0:4], hum_string[0:4]]

    # Control Humidity Relay
    if int(utils.getTempHum(sensor)[0]) < BC.threshold:
        utils.humidityRelayOn(GPIO, BC.pins_dict.get('humidity_relay_pin'))

    else:
        utils.humidityRelayOff(GPIO, BC.pins_dict.get('humidity_relay_pin'))

    # Control Temperature Relay
    # if float(temp_string[0:4])< BC.threshold:
    #     utils.tempRelayOn(GPIO, BC.pins_dict.get('temp_relay_pin'))
    # else:
    #     utils.tempRelayOff(GPIO, BC.pins_dict.get('temp_relay_pin'))

    # Send values to the server
    # send_samples(url=BC.server_url,samples=samples)

    return

def main():
    # count = 0
    textIn = "/home/debian/greenhouse/command.txt"
    print("before")
    utils.humidityRelayOn(GPIO, BC.pins_dict.get('humidity_relay_pin'))
    print("after")
    while True:
        console()


if __name__ == "__main__":
    main()

