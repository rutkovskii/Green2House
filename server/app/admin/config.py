import os
from dotenv import load_dotenv

load_dotenv()

class ServerConfig:
    DATABASE_URI = 'postgresql+psycopg2://ubuntu:ubuntu@0.0.0.0:5455/postgresDB'

    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    FLASK_DIR = os.path.join(ROOT_DIR, '../flask_content')
    FLASK_HTML_DIR = os.path.join(FLASK_DIR, 'HTML')

    # Routes
    HOME_PAGE_ROUTE = '/'
    ADMIN_PAGE_ROUTE = '/admin'
    ADMIN_PAGE_USERS_ROUTE = '/admin/all-users'
    ADMIN_PAGE_SERVE_USERS_ROUTE = '/api/serve-users'
    GET_DATA_ROUTE = '/get-data'
    ADMIN_DATA_SAMPLES_ROUTE = '/admin/all-data-records'

    # Secrets
    ADMINS = [os.getenv('ADMIN1'), os.getenv('ADMIN2')]
    SECRET_KEY = os.getenv('SECRET_KEY')
