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
        'humidity_relay_pin': "P8_10",
        'temp_relay_pin': ""
    }

    # Variables
    threshold = 80
    user_id = 1
    server_url = 'http://172.20.10.5/get_data'

