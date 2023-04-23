import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

from bbb_config import BBB_CONFIG as BC  # pins are here
from scripts.init_home import create_all
from scripts import utils
from scripts.send_data import send_samples

i2c, sensor, oled = create_all(BC.pins_dict)
ADC.setup()

def measureValues():
    value = ADC.READ("AIN4")
    print(value)


def main():
    while True:
        measureValues()
        time.sleep(2)