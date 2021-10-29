# Needed for colorful console output Install with: python3 -m pip install colorama (Mac/Linux) or pip install colorama (PC)
import logging
import os
import time
import threading

from .Logger import Logger
from .helpers.parameters import parse_args
from .broker.BinanceBroker import BinanceBroker
from .strats.volatility.VolatilityStrat import VolatilityStrat
from .helpers.parameters import load_yml
from .helpers.Qist import Qist

def main():
    # Load arguments then parse settings
    args = parse_args()
    base_config = load_yml("config.yml")

    os.environ["PYTHON_ENV"] = base_config["PYTHON_ENV"] if base_config["PYTHON_ENV"] else "production"
    Logger()
    broker = BinanceBroker()
    strat = VolatilityStrat(broker)
