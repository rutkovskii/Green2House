import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import adafruit_ahtx0, adafruit_ssd1306

from bbb_config import BBB_CONFIG as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples

i2c, oled, button = create_all(BC.pins_dict)
sensor = adafruit_ahtx0.AHTx0(i2c)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

#sensor should be included in the above function but because it isn't working I have removed it temporarily

#Do not heavily modify code or BB before MDR

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
        ###COMMENTED OUT FOR MDR###
        sensorF = utils.getTempHum(sensor)[0]
        sensorH = utils.getTempHum(sensor)[1]
        
        #sensorF = 0
        #print("Reading:",ADC.read("AIN0"))
        #sensorC = (ADC.read("AIN0")*1800 - 500)/10
        #sensorF = sensorC*9/5 + 32
        #print(time.strftime('%S'))
        
        print("Temperature: %2.1f°F\nHumidity: %2.0f%%" %(sensorF, sensorH))

        if BC.SEND_DATA:
            # Create Sample to propagate to the database
            sample = utils.sense_sample(BC.user_id,sensorF,sensorH)
            samples = [sample]
            # Send values to the server
            send_samples(url=BC.server_url, samples=samples)

        utils.dispOLED(oled, temp=str(sensorF)[0:4], hum=str(sensorH)[0:4], timestamp=time.strftime('%H:%M:%S'))
        #utils.dispOLED(oled=oled, temp=str(sensorF)[0:4], hum="N/A", timestamp=time.strftime('%H:%M:%S'))
        time.sleep(1)

    # Control Temperature Relay
        if int(sensorF) >= BC.threshold + BC.variance:
            utils.relayOn(GPIO, BC.pins_dict.get('temp_relay_pin'))

        elif int(sensorF) < BC.threshold: #- BC.variance: 
            utils.relayOff(GPIO, BC.pins_dict.get('temp_relay_pin'))

    #water pump relay
    if not (utils.pumpOn(GPIO, BC.pins_dict.get('button_pin'))):
        #print(BC.toggle)
        BC.toggle = 1 - BC.toggle
        time.sleep(0.5)
        if BC.toggle == 1:
            utils.relayOn(GPIO, BC.pins_dict.get('pump_relay_pin'))
            print("pump relay on")

        else:
            utils.relayOff(GPIO, BC.pins_dict.get('pump_relay_pin'))
            print("pump relay off")
        

    return

def main():
    while True:
        console()
        #utils.relayOn(GPIO,BC.pins_dict.get('pump_relay_pin'))


if __name__ == "__main__":
    main()

