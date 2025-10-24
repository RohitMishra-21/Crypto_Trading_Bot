import logging

logger = logging.getLogger(__name__)

def place_market_order(client, symbol: str, side: str, quantity: float):
    logger.info(f"Placing MARKET {side} {quantity} {symbol}")
    order = client.place_order(
        symbol=symbol,
        side=side,
        order_type='MARKET',
        quantity=quantity
    )
    logger.info(f"Order placed id={order.get('orderId')} status={order.get('status')}")
    return order
