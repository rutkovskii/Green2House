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

    # Keys and Secrets
    # SECRET_KEY = os.getenv("SECRET_KEY")

    # with open(os.path.join(CONFIG_DIR, "env.txt")) as e:
    #     ENVIRONMENT = e.read().strip()
    # if ENVIRONMENT == "local":
    #     pass

    # elif ENVIRONMENT == "server":
    #     pass
