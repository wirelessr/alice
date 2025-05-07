import logging
import os

def setup_logging():
    logger = logging.getLogger('alice')
    from config import current_config
    log_level = current_config['ALICE_LOG_LEVEL']
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # Set file handler
    log_file = os.path.join(os.path.dirname(__file__), 'alice.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Remove all existing handlers
    logger.handlers = []

    # Add new handlers
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger