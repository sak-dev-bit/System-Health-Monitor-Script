# logger_setup.py
import logging
from logging.handlers import RotatingFileHandler
import config

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))
    ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(config.LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    fh.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))
    fh.setFormatter(ch_formatter)
    logger.addHandler(fh)

    return logger
