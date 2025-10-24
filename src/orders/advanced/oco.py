import logging

logger = logging.getLogger(__name__)

def place_oco_order(client, symbol: str, side: str, quantity: float, price: float, stop_price: float, stop_limit_price: float, tif: str = 'GTC'):
    """Places a pseudo-OCO order by placing two separate orders (LIMIT and STOP_LIMIT).
    
    WARNING: This is not a true OCO order. If one order is filled, the other will NOT be automatically canceled.
    """
    logger.warning("Placing a pseudo-OCO order. The two orders are not linked.")
    logger.info(f"Placing OCO {side} {quantity} {symbol} at price {price} with stop at {stop_price} and stop-limit at {stop_limit_price}")
    
    orders = []
    
    # Take-profit order
    tp_side = 'SELL' if side.upper() == 'BUY' else 'BUY'
    tp_order = client.place_order(
        symbol=symbol,
        side=tp_side,
        order_type='LIMIT',
        quantity=quantity,
        price=price,
        timeInForce=tif
    )
    logger.info(f"Take-profit order placed: {tp_order}")
    orders.append(tp_order)
    
    # Stop-loss order
    sl_order = client.place_order(
        symbol=symbol,
        side=tp_side,
        order_type='STOP',
        quantity=quantity,
        price=stop_limit_price,
        stopPrice=stop_price,
        timeInForce=tif
    )
    logger.info(f"Stop-loss order placed: {sl_order}")
    orders.append(sl_order)
    
    return orders
