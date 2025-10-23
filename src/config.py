import os
from dotenv import load_dotenv
load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
TESTNET_BASE_URL = os.getenv('TESTNET_BASE_URL', 'https://testnet.binancefuture.com')
DEFAULT_WORKING_TYPE = os.getenv('WORKING_TYPE', 'CONTRACT_PRICE')  # or 'MARK_PRICE'
