
import logging


class LoggingService():

    # FIXME: I am synchronous!

    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    async def log(self, message, *args):
        self.logger.log(self.level, message, *args)
