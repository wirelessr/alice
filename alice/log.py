import logging
import os

def setup_logging():
    logger = logging.getLogger('alice')
    log_level = os.getenv('ALICE_LOG_LEVEL', 'DEBUG').upper()
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 設定console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # 設定file handler
    log_file = os.path.join(os.path.dirname(__file__), 'alice.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 移除所有現有的handler
    logger.handlers = []

    # 加入新的handler
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger