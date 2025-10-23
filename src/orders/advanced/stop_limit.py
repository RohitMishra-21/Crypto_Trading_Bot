from ...logger_config import setup_logger


logger = setup_logger('StopLimit')

def place_stop_limit_order(client, symbol: str, side: str, quantity: float, price: float, stop_price: float, tif: str='GTC'):
    """Futures STOP-LIMIT uses type='STOP' with price + stopPrice."""
    logger.info(f"Placing STOP-LIMIT {side} {quantity} {symbol} stop@{stop_price} limit@{price}")
    order = client.place_order(
        symbol=symbol,
        side=side,
        order_type='STOP',
        quantity=quantity,
        price=price,
        stopPrice=stop_price,
        timeInForce=tif
    )
    logger.info(f"Order placed id={order.get('orderId')} status={order.get('status')}")
    return order
