import logging
import os

def setup_logging():
    logger = logging.getLogger('alice')
    from alice.config import current_config
    log_level = current_config['ALICE_LOG_LEVEL']
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # Remove all existing handlers
    logger.handlers = []

    # Add new handler (console only)
    logger.addHandler(ch)

    return logger