import time

from helpers.parameters import load_yml
from ..IStrat import IStrat
import logging
from typing import Dict

from ...broker.IBroker import IBroker


class VolatilityStrat(IStrat):
    def __init__(self, broker: IBroker):
        super().__init__(broker)
        logging.info("Initializing VolatilityStrat")
        self.__config = load_yml(filepath="/home/thomas/documents/trading-bot/flr/strats/volatility/config.yml")
        self.symbols = self.broker.get_symbols(pair_with=self.__config["PAIR_WITH"],
                                          excluded=self.__config["EXCLUDED"],
                                          custom_list=self.__config["SELECTED"])
        logging.info("VolatilityStrat, ready to comply.")

    def loop(self):
        logging.info("looping")

    def run(self):
        while True:
            self.loop()
            time.sleep(2)
