import logging
from datetime import datetime
from binance.client import Client, BinanceAPIException
from typing import Dict, List, Optional

from .IBroker import IBroker
from ..helpers.parameters import load_yml

DEFAULT_CREDS_FILEPATH = 'creds.yml'

class BinanceBroker(IBroker):
    def __init__(self, creds_filepath: str = None):
        super().__init__()
        self.api_key: str = ""
        self.api_secret: str = ""
        self.creds: Dict[str, str] = {}

        self.creds_filepath = creds_filepath if (creds_filepath is not None) else DEFAULT_CREDS_FILEPATH
        self._load_creds()

        self.client = Client(self.api_key, self.api_secret)
        if self._test_api_key() is False:
            raise Exception()


    def _load_creds(self):
        try:
            parsed_creds = load_yml(self.creds_filepath)
        except FileNotFoundError:
            raise Exception(f"credential file(${self.creds_filepath}) not found")
        self.api_key = parsed_creds["binance"]["prod"]["access_key"]
        self.api_secret = parsed_creds["binance"]["prod"]["secret_key"]

    def _test_api_key(self) -> bool:
        try:
            self.client.get_account()
            logging.info("API key validated successfully")
            return True

        except BinanceAPIException as e:
            if e.code == -2015:
                logging.error("Your API key is not formatted correctly...")
            elif e.code == -2021:
                issue = "https://github.com/CyberPunkMetalHead/Binance-volatility-trading-bot/issues/28"
                desc = "Ensure your OS is time synced with a timeserver. See issue."
                logging.error(f"Timestamp for this request was 1000ms ahead of the server's time.\n  {issue}\n  {desc}")
            else:
                logging.error(e)
            return False

        except Exception as e:
            logging.error(f"Fallback exception occurred:\n{e}")
            return False


    def convert_volume(self, quantity: float, value_name: str) -> float:
        """ Converts the volume given in QUANTITY from USDT to coin"""
        raise NotImplementedError

    def market_buy(self):
        raise NotImplementedError

    def market_sell(self):
        raise NotImplementedError

    def get_prices(self, symbols: List[str]):
        coins = self.client.get_all_tickers()
        sample_time = datetime.now()

        filtered_prices = [{"coin": coin, "time": sample_time} for coin in coins if any(symbol == coin["symbol"] for symbol in symbols)]
        return filtered_prices

    def get_symbols(self, pair_with: str, excluded: Optional[List[str]] = None, custom_list: Optional[List[str]] = None) -> List[str]:
        symbols: List[str]
        tickers = self.client.get_all_tickers()

        if custom_list:
            symbols = [ticker["symbol"] for ticker in tickers if any((item + pair_with == ticker["symbol"]) for item in custom_list)]
        else:
            symbols = [ticker["symbol"] for ticker in tickers if pair_with in ticker["symbol"]]
        if excluded:
            symbols = [symbol for symbol in symbols if all(item not in symbol for item in excluded)]
        symbols.sort()

        return symbols

