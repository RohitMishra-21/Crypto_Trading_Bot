import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'logs')
    log_dir = os.path.abspath(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.DEBUG)

    # File handler (rotating)
    fh = RotatingFileHandler(os.path.join(log_dir, 'bot.log'), maxBytes=2_000_000, backupCount=3)
    fh.setLevel(logging.DEBUG)
    ffmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(ffmt)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    cfmt = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(cfmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
