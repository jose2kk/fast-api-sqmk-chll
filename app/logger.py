import logging

from app.settings import (
    LOG_LEVEL,
    SERVICE_NAME,
)

DEFAULT_FORMAT = ("%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s")


def setup_logger():
    logger_instance = logging.getLogger(SERVICE_NAME)
    logger_instance.setLevel(LOG_LEVEL)
    logging.basicConfig(format=DEFAULT_FORMAT)

    return logger_instance


logger = setup_logger()
