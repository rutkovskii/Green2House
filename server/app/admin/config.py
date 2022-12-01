import os

DATABASE_URI = 'postgresql+psycopg2://ubuntu:ubuntu@0.0.0.0:5432/main_db'

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_DIR = os.path.join(ROOT_DIR, '../flask_content')
FLASK_HTML_DIR = os.path.join(FLASK_DIR,'HTML')