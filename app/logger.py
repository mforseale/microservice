import logging
import os

def setup_logger():
    """Setup application logger"""
    logger = logging.getLogger('microservice')
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger