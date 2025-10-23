from ..logger_config import setup_logger


logger = setup_logger('LimitOrder')

def place_limit_order(client, symbol: str, side: str, quantity: float, price: float, tif: str='GTC'):
    logger.info(f"Placing LIMIT {side} {quantity} {symbol} @ {price} {tif}")
    order = client.place_order(
        symbol=symbol,
        side=side,
        order_type='LIMIT',
        quantity=quantity,
        price=price,
        timeInForce=tif
    )
    logger.info(f"Order placed id={order.get('orderId')} status={order.get('status')}")
    return order
