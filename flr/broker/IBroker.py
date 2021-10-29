from typing import List, Optional

class IBroker:
    def __init__(self) -> None:
        pass

    def _load_creds(self):
        raise NotImplementedError

    def _test_api_key(self) -> bool:
        raise NotImplementedError

    def convert_volume(self, quantity: float, value_name: str) -> float:
        raise NotImplementedError

    def market_buy(self):
        raise NotImplementedError

    def market_sell(self):
        raise NotImplementedError

    def get_prices(self, symbols: List[str]):
        raise NotImplementedError

    def get_symbols(self, pair_with: str, excluded: Optional[List[str]] = None, custom_list: Optional[List[str]] = None) -> List[str]:
        raise NotImplementedError