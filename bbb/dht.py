import time, os, csv, sys
import board
import Adafruit_BBIO.GPIO as GPIO
import adafruit_ahtx0, adafruit_ssd1306
import busio as io


threshold = 80

GPIO.setup("P9_15", GPIO.OUT)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)
auto = True
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


def isCommand(file_path): #detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True


def console(usr_cmd): #process user command
    #file = open(input, "r+")
    parse = usr_cmd.split(" ")

    for i in range(0, len(parse)):
        parse[i] = parse[i].strip()

    #parse[0] = parse[0].strip()
    if parse[0] == "info": #display temperature and humidity data
        sensorF = sensor.temperature*9/5+32
        sensorH = sensor.relative_humidity
        print("Temperature: %2.1f°F\nHumidity: %2.0f%%" %(sensorF, sensorH))

        temp_string = str(round(sensorF, 1))
        hum_string = str(sensorH)
        dataRow = [time.strftime('%m/%d/%Y %H:%M:%S'), temp_string[0:4], hum_string[0:4]]

        file = "data.csv"
        csv_file = open(file, 'a')
        csv_write = csv.writer(csv_file)
        csv_write.writerow(dataRow)

        oled.fill(0)
        oled.text("Temperature: "+temp_string[0:4]+"F", 0, 0, color=1)
        oled.text("Humidity: "+hum_string[0:4]+"%", 0, 10, color=1)
        #oled.text(str(round(sensorF, 1)), 0, 20, color=1)
        oled.show()

        if float(temp_string[0:4])<threshold:
            GPIO.output("P9_15", GPIO.HIGH)
        else:
            GPIO.output("P9_15", GPIO.LOW)

    return

#def

def main():
    #count = 0
    textIn = "/home/debian/greenhouse/command.txt"

    while True:
        # if isCommand(textIn): #command detected in txt file
        #     cmdRead = open(textIn, 'r+')
        #     cmd = cmdRead.read()
        #     console(cmd)
        #     cmdRead.truncate(0)

        # line = str(sys.stdin.readline()) #command detected from stdin
        # if line:
        #     console(line)
        console("info")
        time.sleep(10)


if __name__ == "__main__":
    main()

