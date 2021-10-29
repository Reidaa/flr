import json
import os
from binance.client import Client
import time

from .helpers.parameters import load_yml
from .helpers.handle_creds import load_correct_creds

DEFAULT_CONFIG_FILE = 'config.yml'
DEFAULT_CREDS_FILE = 'creds.yml'

class Bot:
    def __init__(self, config_file, creds_file, debug=False) -> None:

        self.config_file = config_file if (config_file is not None) else DEFAULT_CONFIG_FILE
        self.creds_file = creds_file if (creds_file is not None) else DEFAULT_CREDS_FILE

        self.parsed_config = load_yml(self.config_file)
        self.parsed_creds = load_yml(self.creds_file)

        self.DEBUG = False
        self.tickers = None
        self.session_profit = 0

        self._load_system_vars()
        self._load_trading_vars()

        if self.DEBUG_SETTING or debug:
            self.DEBUG = True

        self._load_creds()

        if self.DEBUG:
            print(f'loaded config below\n{json.dumps(self.parsed_config, indent=4)}')
            print(f'Your credentials have been loaded from {self.creds_file}')

        self.client = Client(self.access_key, self.secret_key)

        if self.CUSTOM_LIST:
            self.tickers = [line.strip() for line in open('tickers.txt')]

        # try to load all the coins bought by the bot if the file exists and is not empty
        self.coins_bought = {}
        # path to the saved coins_bought file
        self.coins_bought_file_path = 'coins_bought.json'

        # rolling window of prices; cyclical queue
        self.historical_prices = [None] * (self.TIME_DIFFERENCE * self.RECHECK_INTERVAL)
        self.hsp_head = -1

        # prevent including a coin in volatile_coins if it has already appeared there less than TIME_DIFFERENCE minutes ago
        self.volatility_cooloff = {}

        if self.TEST_MODE:
            self.coins_bought_file_path = 'test_' + self.coins_bought_file_path

        # if saved coins_bought json file exists and it's not empty then load it
        if os.path.isfile(self.coins_bought_file_path) and os.stat(self.coins_bought_file_path).st_size != 0:
            with open(self.coins_bought_file_path) as file:
                self.coins_bought = json.load(file)

        print('Press Ctrl-Q to stop the script')

        if not self.TEST_MODE:
            print('WARNING: You are using the Mainnet and live funds. Waiting 30 seconds as a security measure')
            time.sleep(30)

    def run(self):
        while True:
            pass
        # self.get_price()
        # while True:
        #     orders, last_price, volume = self.buy()
        #     self.update_portfolio(orders, last_price, volume)
        #     coins_sold = self.sell_coins()
        #     self.remove_from_portfolio(coins_sold)

    def _load_system_vars(self):
        # Load system vars
        self.TEST_MODE = self.parsed_config['script_options']['TEST_MODE']
        self.LOG_TRADES = self.parsed_config['script_options'].get('LOG_TRADES')
        self.LOG_FILE = self.parsed_config['script_options'].get('LOG_FILE')
        self.DEBUG_SETTING = self.parsed_config['script_options'].get('DEBUG')

    def _load_trading_vars(self):
        self.PAIR_WITH = self.parsed_config['trading_options']['PAIR_WITH']
        self.QUANTITY = self.parsed_config['trading_options']['QUANTITY']
        self.MAX_COINS = self.parsed_config['trading_options']['MAX_COINS']
        self.FIATS = self.parsed_config['trading_options']['FIATS']
        self.TIME_DIFFERENCE = self.parsed_config['trading_options']['TIME_DIFFERENCE']
        self.RECHECK_INTERVAL = self.parsed_config['trading_options']['RECHECK_INTERVAL']
        self.CHANGE_IN_PRICE = self.parsed_config['trading_options']['CHANGE_IN_PRICE']
        self.STOP_LOSS = self.parsed_config['trading_options']['STOP_LOSS']
        self.TAKE_PROFIT = self.parsed_config['trading_options']['TAKE_PROFIT']
        self.CUSTOM_LIST = self.parsed_config['trading_options']['CUSTOM_LIST']
        self.USE_TRAILING_STOP_LOSS = self.parsed_config['trading_options']['USE_TRAILING_STOP_LOSS']
        self.TRAILING_STOP_LOSS = self.parsed_config['trading_options']['TRAILING_STOP_LOSS']
        self.TRAILING_TAKE_PROFIT = self.parsed_config['trading_options']['TRAILING_TAKE_PROFIT']

    def _load_creds(self):
        self.access_key, self.secret_key = load_correct_creds(self.parsed_creds)

    # def get_price(self, add_to_historical=True):
    #     """Return the current price for all coins on binance"""
    #
    #     initial_price = {}
    #     prices = self.client.get_all_tickers()
    #
    #     for coin in prices:
    #         if self.CUSTOM_LIST:
    #             if any(item + self.PAIR_WITH == coin['symbol'] for item in self.tickers) and all(
    #                     item not in coin['symbol'] for item in self.FIATS):
    #                 initial_price[coin['symbol']] = {'price': coin['price'], 'time': datetime.now()}
    #         else:
    #             if self.PAIR_WITH in coin['symbol'] and all(item not in coin['symbol'] for item in self.FIATS):
    #                 initial_price[coin['symbol']] = {'price': coin['price'], 'time': datetime.now()}
    #
    #     if add_to_historical:
    #         self.hsp_head = (self.hsp_head + 1) % (self.TIME_DIFFERENCE * self.RECHECK_INTERVAL)
    #         self.historical_prices[self.hsp_head] = initial_price
    #
    #     return initial_price
    #
    # def wait_for_price(self):
    #     """calls the initial price and ensures the correct amount of time has passed before reading the current price again"""
    #
    #     volatile_coins = {}
    #
    #     coins_up = 0
    #     coins_down = 0
    #     coins_unchanged = 0
    #
    #     if self.historical_prices[self.hsp_head]['BNB' + self.PAIR_WITH]['time'] > datetime.now() - timedelta(minutes=float(self.TIME_DIFFERENCE / self.RECHECK_INTERVAL)):
    #         # sleep for exactly the amount of time required
    #         time.sleep((timedelta(minutes=float(self.TIME_DIFFERENCE / self.RECHECK_INTERVAL)) - (datetime.now() - self.historical_prices[self.hsp_head]['BNB' + self.PAIR_WITH]['time'])).total_seconds())
    #
    #     print(f'not enough time has passed yet...Session profit:{self.session_profit:.2f}%')
    #
    #     # retreive latest prices
    #     self.get_price()
    #
    #     # calculate the difference in prices
    #     for coin in self.historical_prices[self.hsp_head]:
    #         # minimum and maximum prices over time period
    #         min_price = min(self.historical_prices, key=lambda x: float("inf") if x is None else float(x[coin]['price']))
    #         max_price = max(self.historical_prices, key=lambda x: -1 if x is None else float(x[coin]['price']))
    #
    #         threshold_check = (-1.0 if min_price[coin]['time'] > max_price[coin]['time'] else 1.0) * (
    #                     float(max_price[coin]['price']) - float(min_price[coin]['price'])) / float(
    #             min_price[coin]['price']) * 100
    #
    #         # each coin with higher gains than our CHANGE_IN_PRICE is added to the volatile_coins dict if less than MAX_COINS is not reached.
    #         if threshold_check > self.CHANGE_IN_PRICE:
    #             coins_up += 1
    #
    #             if coin not in self.volatility_cooloff:
    #                 self.volatility_cooloff[coin] = datetime.now() - timedelta(minutes=self.TIME_DIFFERENCE)
    #
    #             # only include coin as volatile if it hasn't been picked up in the last TIME_DIFFERENCE minutes already
    #             if datetime.now() >= self.volatility_cooloff[coin] + timedelta(minutes=self.TIME_DIFFERENCE):
    #                 self.volatility_cooloff[coin] = datetime.now()
    #
    #                 if len(self.coins_bought) + len(volatile_coins) < self.MAX_COINS or self.MAX_COINS == 0:
    #                     volatile_coins[coin] = round(threshold_check, 3)
    #                     print(
    #                         f'{coin} has gained {volatile_coins[coin]}% within the last {self.TIME_DIFFERENCE} minutes, calculating volume in {self.PAIR_WITH}')
    #
    #                 else:
    #                     print(
    #                         f'{txcolors.WARNING}{coin} has gained {round(threshold_check, 3)}% within the last {self.TIME_DIFFERENCE} minutes, but you are holding max number of coins{txcolors.DEFAULT}')
    #
    #         elif threshold_check < self.CHANGE_IN_PRICE:
    #             coins_down += 1
    #
    #         else:
    #             coins_unchanged += 1
    #
    #     print(f'Up: {coins_up} Down: {coins_down} Unchanged: {coins_unchanged}')
    #
    #     return volatile_coins, len(volatile_coins), self.historical_prices[self.hsp_head]
    #
    # def convert_volume(self):
    #     """Converts the volume given in QUANTITY from USDT to the each coin's volume"""
    #
    #     volatile_coins, number_of_coins, last_price = self.wait_for_price()
    #     lot_size = {}
    #     volume = {}
    #
    #     for coin in volatile_coins:
    #
    #         # Find the correct step size for each coin
    #         # max accuracy for BTC for example is 6 decimal points
    #         # while XRP is only 1
    #         try:
    #             info = self.client.get_symbol_info(coin)
    #             step_size = info['filters'][2]['stepSize']
    #             lot_size[coin] = step_size.index('1') - 1
    #
    #             if lot_size[coin] < 0:
    #                 lot_size[coin] = 0
    #
    #         except:
    #             pass
    #
    #         # calculate the volume in coin from QUANTITY in USDT (default)
    #         volume[coin] = float(self.QUANTITY / float(last_price[coin]['price']))
    #
    #         # define the volume with the correct step size
    #         if coin not in lot_size:
    #             volume[coin] = float('{:.1f}'.format(volume[coin]))
    #
    #         else:
    #             # if lot size has 0 decimal points, make the volume an integer
    #             if lot_size[coin] == 0:
    #                 volume[coin] = int(volume[coin])
    #             else:
    #                 volume[coin] = float('{:.{}f}'.format(volume[coin], lot_size[coin]))
    #
    #     return volume, last_price
    #
    # def buy(self):
    #     """Place Buy market orders for each volatile coin found"""
    #
    #     volume, last_price = self.convert_volume()
    #     orders = {}
    #
    #     for coin in volume:
    #
    #         # only buy if the there are no active trades on the coin
    #         if coin not in self.coins_bought:
    #             self.log(f"{txcolors.BUY}Preparing to buy {volume[coin]} {coin}{txcolors.DEFAULT}")
    #
    #             if self.TEST_MODE:
    #                 orders[coin] = [{
    #                     'symbol': coin,
    #                     'orderId': 0,
    #                     'time': datetime.now().timestamp()
    #                 }]
    #
    #                 # Log trade
    #                 if self.LOG_TRADES:
    #                     self.log_trade(self.LOG_FILE, f"Buy : {volume[coin]} {coin} - {last_price[coin]['price']}")
    #
    #                 continue
    #
    #             # try to create a real order if the tests orders did not raise an exception
    #             try:
    #                 buy_limit = self.client.create_order(
    #                     symbol=coin,
    #                     side='BUY',
    #                     type='MARKET',
    #                     quantity=volume[coin]
    #                 )
    #
    #             # error handling here in case position cannot be placed
    #             except Exception as e:
    #                 self.log(e)
    #
    #             # run the else block if the position has been placed and return order info
    #             else:
    #                 orders[coin] = self.client.get_all_orders(symbol=coin, limit=1)
    #
    #                 # binance sometimes returns an empty list, the code will wait here until binance returns the order
    #                 while orders[coin] == []:
    #                     self.log('Binance is being slow in returning the order, calling the API again...')
    #
    #                     orders[coin] = self.client.get_all_orders(symbol=coin, limit=1)
    #                     time.sleep(1)
    #
    #                 else:
    #                     self.log('Order returned, saving order to file')
    #
    #                     # Log trade
    #                     if self.LOG_TRADES:
    #                         write_log(self.LOG_FILE, f"Buy : {volume[coin]} {coin} - {last_price[coin]['price']}")
    #         else:
    #             self.log(f'Signal detected, but there is already an active trade on {coin}')
    #
    #     return orders, last_price, volume
    #
    # def sell_coins(self):
    #     """sell coins that have reached the STOP LOSS or TAKE PROFIT threshold"""
    #
    #     last_price = self.get_price(False)  # don't populate rolling window
    #     coins_sold = {}
    #
    #     for coin in list(self.coins_bought):
    #         # define stop loss and take profit
    #         TP = float(self.coins_bought[coin]['bought_at']) + (
    #                     float(self.coins_bought[coin]['bought_at']) * self.coins_bought[coin]['take_profit']) / 100
    #         SL = float(self.coins_bought[coin]['bought_at']) + (
    #                     float(self.coins_bought[coin]['bought_at']) * self.coins_bought[coin]['stop_loss']) / 100
    #
    #         last_price = float(last_price[coin]['price'])
    #         buy_price = float(self.coins_bought[coin]['bought_at'])
    #         price_change = float((last_price - buy_price) / buy_price * 100)
    #
    #         # check that the price is above the take profit and readjust SL and TP accordingly if trialing stop loss used
    #         if float(last_price[coin]['price']) > TP and self.USE_TRAILING_STOP_LOSS:
    #             if self.DEBUG: print("TP reached, adjusting TP and SL accordingly to lock-in profit")
    #
    #             # increasing TP by TRAILING_TAKE_PROFIT (essentially next time to readjust SL)
    #             self.coins_bought[coin]['take_profit'] += self.TRAILING_TAKE_PROFIT
    #             self.coins_bought[coin]['stop_loss'] = self.coins_bought[coin]['take_profit'] - self.TRAILING_STOP_LOSS
    #
    #             continue
    #
    #         # check that the price is below the stop loss or above take profit (if trailing stop loss not used) and sell if this is the case
    #         if float(last_price[coin]['price']) < SL or (
    #                 float(last_price[coin]['price']) > TP and not self.USE_TRAILING_STOP_LOSS):
    #             print(
    #                 f"{txcolors.SELL_PROFIT if price_change >= 0. else txcolors.SELL_LOSS}TP or SL reached, selling {self.coins_bought[coin]['volume']} {coin} - {buy_price} - {last_price} : {price_change:.2f}%{txcolors.DEFAULT}")
    #
    #             # try to create a real order
    #             try:
    #                 if not self.TEST_MODE:
    #                     sell_coins_limit = self.client.create_order(
    #                         symbol=coin,
    #                         side='SELL',
    #                         type='MARKET',
    #                         quantity=self.coins_bought[coin]['volume']
    #                     )
    #
    #             # error handling here in case position cannot be placed
    #             except Exception as e:
    #                 print(e)
    #
    #             # run the else block if coin has been sold and create a dict for each coin sold
    #             else:
    #                 coins_sold[coin] = self.coins_bought[coin]
    #                 # Log trade
    #
    #                 if self.LOG_TRADES:
    #                     profit = (last_price - buy_price) * coins_sold[coin]['volume']
    #                     self.log_trade(self.LOG_FILE,
    #                         f"Sell: {coins_sold[coin]['volume']} {coin} - {buy_price} - {last_price} Profit: {profit:.2f} {price_change:.2f}%")
    #                     self.session_profit = self.session_profit + price_change
    #             continue
    #
    #         # no action; print once every TIME_DIFFERENCE
    #         if self.hsp_head == 1:
    #             self.log(
    #                 f'TP or SL not yet reached, not selling {coin} for now {buy_price} - {last_price} : {txcolors.SELL_PROFIT if price_change >= 0. else txcolors.SELL_LOSS}{price_change:.2f}%{txcolors.DEFAULT}')
    #
    #     return coins_sold
    #
    # def update_portfolio(self, orders, last_price, volume):
    #     """add every coin bought to our portfolio for tracking/selling later"""
    #
    #     if self.DEBUG:
    #         self.log(orders)
    #     for coin in orders:
    #         self.coins_bought[coin] = {
    #             'symbol': orders[coin][0]['symbol'],
    #             'orderid': orders[coin][0]['orderId'],
    #             'timestamp': orders[coin][0]['time'],
    #             'bought_at': last_price[coin]['price'],
    #             'volume': volume[coin],
    #             'stop_loss': -self.STOP_LOSS,
    #             'take_profit': self.TAKE_PROFIT,
    #         }
    #
    #         # save the coins in a json file in the same directory
    #         with open(self.coins_bought_file_path, 'w') as file:
    #             json.dump(self.coins_bought, file, indent=4)
    #
    #         self.log(f'Order with id {orders[coin][0]["orderId"]} placed and saved to file')
    #
    # def remove_from_portfolio(self, coins_sold):
    #     """Remove coins sold due to SL or TP from portfolio"""
    #     for coin in coins_sold:
    #         self.coins_bought.pop(coin)
    #
    #     with open(self.coins_bought_file_path, 'w') as file:
    #         json.dump(self.coins_bought, file, indent=4)
    #