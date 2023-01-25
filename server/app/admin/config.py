import os


class SERVER_CONFIG():
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
    ALL_DATS_SAMPLES_ROUTE = '/all-data-samples'
    SERVE_DATA_SAMPLES_ROUTE = '/api/serve-data-samples'
