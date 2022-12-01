import time, os, csv, sys
import Adafruit_BBIO.GPIO as GPIO

from send_data import send_samples
from init_home import create_all
import utils # import isCommand, single_float_pt, getTempHum, dispOLED, sense_sample, relayOn, relayOff

threshold = 80
user_id = 1
dest_url = 'http://172.20.10.5/get_data'

relayPin = "P8_10"

i2c, sensor, oled = create_all(relayPin)


#############################
# Created utils.py — with sensing funcitons
# Created init_home.py — to initialize the sensor, OLED, i2c, and do set up of GPIO and ADC
# Modified sensing functions a bit to make them more modular
# Created sense_sample() to create a sample
# Modifed send_sample_data() to send_samples()

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

        # sample = sense_sample(user_id,sensorF,sensorH)
        # samples = [sample]

        utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum=str(sensorH)[0:4], timestamp=time.strftime('%H:%M:%S'))
        time.sleep(8)

        # temp_string = str(round(sensorF, 1))
        # hum_string = str(sensorH)
        # dataRow = [time.strftime('%m/%d/%Y %H:%M:%S'), temp_string[0:4], hum_string[0:4]]
    
    if(int(utils.getTempHum(sensor)[0]) < threshold):
        utils.relayOn(GPIO, relayPin)

    else:
        utils.relayOff(GPIO, relayPin)

    # send_samples(url=dest_url,samples=samples)

    # if float(temp_string[0:4])<threshold:
    #     GPIO.output("P9_15", GPIO.HIGH)
    # else:
    #     GPIO.output("P9_15", GPIO.LOW)

    return

def main():
    # count = 0
    textIn = "/home/debian/greenhouse/command.txt"
    print("before")
    utils.relayOn(GPIO, relayPin)
    print("after")
    while True:
        console()


if __name__ == "__main__":
    main()

