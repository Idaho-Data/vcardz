import logging

def set_logger(level=logging.WARNING):
    log_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    formatter = logging.Formatter(log_format, '%Y-%m-%dT%H:%M:%S%Z')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(logging.Filter(name='vcardz'))

    logging.basicConfig(level=level,
                        handlers=[stream_handler])    

def get_logger():
    logger = logging.getLogger('vcardz')
    logger.addFilter(logging.Filter(name='vcardz'))
    return logger

    


