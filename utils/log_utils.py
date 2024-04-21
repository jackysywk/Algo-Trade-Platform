import logging
from logging.handlers import RotatingFileHandler
import os

# Define the log direcotry and filename



def setup_logger(LoggerName, log_dir = '../log',log_file = 'program.log'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger(LoggerName)
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir,log_file), maxBytes=10485760, backupCount=5
    )

    file_handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger