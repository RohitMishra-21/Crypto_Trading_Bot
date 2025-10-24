import argparse
import logging
from .client import BinanceClient
from .validator import validate_and_normalize
from .orders.market_orders import place_market_order
from .orders.limit_orders import place_limit_order
from .orders.advanced.stop_limit import place_stop_limit_order
from .orders.advanced.twap import place_twap_orders
from .orders.advanced.oco import place_oco_order
from .logger_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def main():
    p = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')
    p.add_argument('symbol', help='e.g., BTCUSDT')
    p.add_argument('side', help='BUY or SELL')
    p.add_argument('order_type', help='MARKET, LIMIT, STOP_LIMIT, TWAP, OCO')
    p.add_argument('quantity', type=float, help='Order quantity')
    p.add_argument('--price', type=float, help='Limit price (LIMIT/STOP_LIMIT/TWAP/OCO)')
    p.add_argument('--stop-price', type=float, help='Stop trigger price (STOP_LIMIT/OCO)')
    p.add_argument('--stop-limit-price', type=float, help='Stop limit price (OCO)')
    p.add_argument('--tif', default='GTC', help='Time in force (default GTC)')
    p.add_argument('--chunks', type=int, default=1, help='TWAP chunks')
    p.add_argument('--interval', type=int, default=30, help='TWAP interval seconds')
    args = p.parse_args()

    client = BinanceClient(testnet=True)

    qty, px, stop_px, stop_limit_px = validate_and_normalize(client, args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price, args.stop_limit_price)

    if args.order_type.upper() == 'MARKET':
        order = place_market_order(client, args.symbol, args.side, qty)
    elif args.order_type.upper() == 'LIMIT':
        order = place_limit_order(client, args.symbol, args.side, qty, px, args.tif)
    elif args.order_type.upper() == 'STOP_LIMIT':
        order = place_stop_limit_order(client, args.symbol, args.side, qty, px, stop_px, args.tif)
    elif args.order_type.upper() == 'TWAP':
        order = place_twap_orders(client, args.symbol, args.side, qty, px, args.chunks, args.interval, args.tif)
    elif args.order_type.upper() == 'OCO':
        order = place_oco_order(client, args.symbol, args.side, qty, px, stop_px, stop_limit_px, args.tif)
    else:
        raise SystemExit('Unsupported order_type')

    print('Order Result:', order)

if __name__ == '__main__':
    main()
    logging.shutdown()
