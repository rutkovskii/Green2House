import time, os, csv, sys
from datetime import datetime as dt
from math import floor

import board
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import adafruit_ahtx0, adafruit_ssd1306
import busio as io

from send_data import send_sample_data

threshold = 80

GPIO.setup("P9_15", GPIO.OUT)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)
auto = True
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
ADC.setup()

def isCommand(file_path): #detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True


def single_float_pt(number):
    return floor(number*10)/10

def getTempHum():
    sensorF = sensor.temperature*9/5 + 32 #temp in Fahrenheit
    sensorH = sensor.relative_humidity
    return sensorF, sensorH

def dispOLED(temperature, hum, timestamp):
    oled.fill(0)
    oled.text("Temperature: "+temperature+"F", 0, 0, color=1)
    oled.text("Humidity: "+hum+"%", 0, 10, color=1)
    oled.text(timestamp, 0, 20, color=1)
    oled.show()

    return

def console(usr_cmd): #process user command

    #sensorF = getTempHum()[0]
    #sensorH = getTempHum()[1]

    # temp_string = str(round(sensorF, 1))
    # hum_string = str(sensorH)
    # dataRow = [time.strftime('%m/%d/%Y %H:%M:%S'), temp_string[0:4], hum_string[0:4]]

    # file = "data.csv"
    # csv_file = open(file, 'a')
    # csv_write = csv.writer(csv_file)
    # csv_write.writerow(dataRow)

    if(int(time.strftime('%S'))%10 == 0): #sense data every 10 seconds
        sensorF = getTempHum()[0]
        sensorH = getTempHum()[1]
        #print(time.strftime('%S'))
        print("Temperature: %2.1f°F\nHumidity: %2.0f%%" %(sensorF, sensorH))
        # sample = {'user_id': 1, 'temperature':single_float_pt(sensorF), 'humidity':single_float_pt(sensorH), 'timestamp': int(round(dt.timestamp(dt.now())))}
        # samples = [sample]
        dispOLED(str(sensorF)[0:4], str(sensorH)[0:4], time.strftime('%H:%M:%S'))
        time.sleep(8)
        # temp_string = str(round(sensorF, 1))
        # hum_string = str(sensorH)
        #dataRow = [time.strftime('%m/%d/%Y %H:%M:%S'), temp_string[0:4], hum_string[0:4]]
    
    #send_sample_data(url='http://172.20.10.5/get_data',samples=samples)

    # if float(temp_string[0:4])<threshold:
    #     GPIO.output("P9_15", GPIO.HIGH)
    # else:
    #     GPIO.output("P9_15", GPIO.LOW)

    return

def main():
    #count = 0
    textIn = "/home/debian/greenhouse/command.txt"

    while True:
        console("info")


if __name__ == "__main__":
    main()

