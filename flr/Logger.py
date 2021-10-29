import logging
import os

class txcolors:
    BUY = '\033[92m'
    WARNING = '\033[93m'
    SELL_LOSS = '\033[91m'
    SELL_PROFIT = '\033[32m'
    DIM = '\033[2m\033[35m'
    DEFAULT = '\033[39m'

class Logger:
    def __init__(self):
        self.log_format: str = ""

        if os.environ.get("PYTHON_ENV") == "production":
            self._production()
        elif os.environ.get("PYTHON_ENV") == "development":
            self._development()
        elif os.environ.get("PYTHON_ENV") == "test":
            self._test()
        else:
            raise Exception("Wrong PYTHON_ENV value")

    def _production(self):
        self.log_format = logging.Formatter("[%(asctime)s] %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler("info.log", "w")
        self.file_handler.setLevel(logging.INFO)

        self.console_handler.setFormatter(self.log_format)
        self.file_handler.setFormatter(self.log_format)

        # self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)


    def _development(self):
        self.log_format = "[%(asctime)s] %(levelname)s:%(pathname)s: %(message)s"
        logging.basicConfig(format=self.log_format, level=logging.DEBUG)

    def _test(self):
        self._development()
