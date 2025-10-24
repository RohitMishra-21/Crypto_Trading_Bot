from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .config import BINANCE_API_KEY, BINANCE_API_SECRET, TESTNET_BASE_URL, DEFAULT_WORKING_TYPE
import logging

class BinanceClient:
    """
    Thin wrapper over python-binance for UM Futures Testnet.
    """
    def __init__(self, testnet: bool = True):
        self.logger = logging.getLogger(__name__)
        requests_params = {'timeout': 30}
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, requests_params=requests_params)
        # Point the futures base URL to testnet (UM: /fapi)
        if testnet:
            self.client.FUTURES_URL = TESTNET_BASE_URL.rstrip('/') + '/fapi'
            self.client.FUTURES_DATA_URL = self.client.FUTURES_URL
        # Ensure one-way mode (not dual)
        try:
            self.client.futures_change_position_mode(dualSidePosition=False)
        except Exception as e:
            self.logger.debug(f"Could not change position mode (maybe already set): {e}")

    def exchange_info(self):
        return self.client.futures_exchange_info()

    def symbol_info(self, symbol: str):
        info = self.exchange_info()
        for s in info['symbols']:
            if s['symbol'].upper() == symbol.upper():
                return s
        return None

    def place_order(self, symbol: str, side: str, order_type: str, **kwargs):
        try:
            # Ensure workingType is set for stop/tp orders where relevant
            if 'workingType' not in kwargs:
                kwargs['workingType'] = DEFAULT_WORKING_TYPE
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type=order_type.upper(),
                **kwargs
            )
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.error(f"API error placing order: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing order: {e}")
            raise

    def place_oco_order(self, **kwargs):
        try:
            order = self.client.futures_create_oco_order(**kwargs)
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.error(f"API error placing OCO order: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing OCO order: {e}")
            raise

    def cancel_order(self, symbol: str, order_id: int):
        return self.client.futures_cancel_order(symbol=symbol.upper(), orderId=order_id)

    def get_price(self, symbol: str):
        return float(self.client.futures_symbol_ticker(symbol=symbol.upper())['price'])
