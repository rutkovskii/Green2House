import logging
import os
from config import Config


def setup_logger(name, log_file, level=logging.DEBUG):
    logs_directory = os.path.join(Config.LOGS_DIR)
    os.makedirs(logs_directory, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_file_path = os.path.join(logs_directory, log_file)

    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
