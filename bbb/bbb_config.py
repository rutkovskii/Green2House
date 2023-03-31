import os
# from dotenv import load_dotenv


class BBB_Config:
    # Locations
    BBB_DIR = os.path.abspath(os.path.dirname(__file__))
    FILES_DIR = os.path.join(BBB_DIR, 'files')
    CONFIG_DIR = os.path.join(BBB_DIR, 'configs')
    # DATA_DIR = os.path.join(SCRIPTS_DIR,'data')
    # LOG_DIR = os.path.join(SCRIPTS_DIR,'logs')

    # Files
    # font_adafruit = os.path.join(FILES_DIR, 'font5x8.bin')
    # print(font_adafruit)

    # Pins
    pins_dict = {
        'h_bridge1': "P8_12",
        'h_bridge2': "P8_14",
        'pump_relay_pin': "P8_16",
        'fan_relay_pin': "P8_18",
        'heater_relay_pin': "P8_26",
        'adc_pin': "AIN6",
        'button_pin': "P9_15"
    }

    # Variables
    desiredTemp = 75  # desired temperature in degrees F
    desiredHum = 50  # desired humidity in percentage RH
    toggle = 0
    user_id = 6
    tempVariance = 1

    min_temperature = 73
    max_temperature = 75
    min_humidity = 20
    max_humidity = 50

    # minADC = wet, maxADC = dry
    minADC = 1450  # the lowest value I measured with the soil moisture sensor
    maxADC = 3250  # the highest value I measured with the soil moisture sensor

    # change link based on ngrok
    # must have internet connection
    SERVER_URL = "https://365f-2600-387-f-5f16-00-5.ngrok.io"
    SERVER_GET_DATA_URL = SERVER_URL + "/get-data"
    SEND_DATA = True

    # Database
    DATABASE_LOCATION = os.path.join(BBB_DIR, 'database.sqlite')
    DATABASE_URI = f'sqlite:///{DATABASE_LOCATION}'
