import time
import board
import adafruit_ahtx0
import datetime as dt
import os
import sys
import Adafruit_BBIO.GPIO as GPIO
GPIO.setup("P9_15", GPIO.OUT)
import adafruit_ssd1306
import busio as io
import class
threshold = 80
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)
auto = True
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def isCommand(file_path): #detect presence of commands
    if os.stat(file_path).st_size == 0:
        return False
    return True

def console(user_cmd):
    print(user_cmd)

def main():
    textIn = "/home/debian/greenhouse/command.txt"

    while True:
        if isCommand(textIn):
            print(textIn)
            cmdRead = open(textIn, 'r+')
            cmd = cmdRead.read()
            console(cmd)
            cmdRead.truncate(0)

        line = str(sys.stdin.readline())
        if line:
            console(line)

    #blah blah blah

if __name__ == "__main__":
    main()