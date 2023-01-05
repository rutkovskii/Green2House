import os
# from dotenv import load_dotenv

class Config:
    # Locations
    SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_DIR = os.path.join(SCRIPTS_DIR,'configs')

    print(CONFIG_DIR)

    # Keys and Secrets
    # FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    with open(os.path.join(CONFIG_DIR, 'env.txt')) as e:
        ENVIRONMENT = e.read().strip()
    if ENVIRONMENT == 'local':
        pass

    elif ENVIRONMENT == 'server':
        pass

