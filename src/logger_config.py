import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler

def setup_logger() -> logging.Logger:
    # Use a temporary directory for debugging file write issues
    log_dir = os.path.join(tempfile.gettempdir(), 'binance_bot_logs')
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.DEBUG)

    # File handler
    log_file_path = os.path.join(log_dir, 'bot.log')
    fh = logging.FileHandler(log_file_path)
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
