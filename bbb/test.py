import time
import board
import busio as io

i2c = io.I2C(board.SCL, board.SDA)

import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(1)
oled.show()
oled.text("Hello", 0, 0, color=0)
oled.show()
time.sleep(1)
oled.fill(0)
oled.show()
