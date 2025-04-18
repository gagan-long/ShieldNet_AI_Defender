import logging

def setup_logging():
    logging.basicConfig(
        filename='shieldnet.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
