import os
# from dotenv import load_dotenv


class BBB_CONFIG:
    # Locations
    BBB_DIR = os.path.abspath(os.path.dirname(__file__))
    FILES_DIR = os.path.join(BBB_DIR, 'files')
    # CONFIG_DIR = os.path.join(SCRIPTS_DIR,'configs')
    # DATA_DIR = os.path.join(SCRIPTS_DIR,'data')
    # LOG_DIR = os.path.join(SCRIPTS_DIR,'logs')

    # Files
    font_adafruit = os.path.join(FILES_DIR, 'font5x8.bin')

    # Pins
    pins_dict = {
        'pump_relay_pin': "P8_8",
        'temp_relay_pin': "P8_10",
        'button_pin': "P8_14"
    }

    # Variables
    threshold = 75
    toggle = 0
    user_id = 1
    variance = 1

    # change link based on ngrok
    # must have internet connection
    SERVER_URL = "https://e3e6-128-119-202-230.ngrok.io"
    SERVER_GET_DATA_URL = SERVER_URL + "/get_data"
    SEND_DATA = False

