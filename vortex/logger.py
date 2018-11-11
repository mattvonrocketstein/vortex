""" vortex.logger
"""
import logging


def get_logger(name):
    logger = logging.getLogger(name.ljust(6))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


class Loggable(object):
    def __init__(self, *args, **kargs):
        self.logger = get_logger(self.__class__.__name__)

    def debug(self, msg, **kargs):
        divider = kargs.pop('divider', False)
        divider = '-' * 50 if divider else ''
        msg = divider + msg
        return self.logger.debug(msg, **kargs)


LOGGER = get_logger('app')
