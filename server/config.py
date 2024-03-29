import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Locations
    SERVER_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_DIR = os.path.join(SERVER_DIR, "configs")
    VOLUMES_DIR = os.path.join(SERVER_DIR, "volumes")
    LOGS_DIR = os.path.join(VOLUMES_DIR, "logs")

    ENVIRONMENT = os.getenv("ENVIRONMENT")
    DATABASE_URI = "postgresql+psycopg2://ubuntu:ubuntu@postgres:5432/postgresDB"
