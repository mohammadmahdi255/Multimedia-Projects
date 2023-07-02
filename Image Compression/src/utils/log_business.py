import logging

import colorama as colorama
from colorama import Fore


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        colors = {"DEBUG": Fore.BLUE, "INFO": Fore.GREEN,
                  "WARNING": Fore.YELLOW, "ERROR": Fore.RED, "CRITICAL": Fore.MAGENTA}
        msg = logging.Formatter.format(self, record)
        if record.levelname in colors:
            msg = colors[record.levelname] + msg + Fore.RESET
        return msg


class MyLogger:
    def __init__(self, name, address=None):
        colorama.init(autoreset=True)
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
        if address:
            file_handler = logging.FileHandler(address, mode='w')
            file_handler.setLevel(logging.DEBUG)  # set file handler level to DEBUG
            file_handler.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
            self.logger.addHandler(file_handler)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)
