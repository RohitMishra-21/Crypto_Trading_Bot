import time
from ...logger_config import setup_logger

logger = setup_logger('TWAP')

def place_twap_orders(client, symbol: str, side: str, total_quantity: float, price: float, chunks: int, interval_seconds: int, tif: str='GTC'):
    assert chunks >= 1, "chunks must be >= 1"
    per = total_quantity / chunks
    logger.info(f"TWAP {side} total={total_quantity} {symbol} in {chunks} chunks every {interval_seconds}s @ {price}")
    results = []
    for i in range(chunks):
        logger.info(f"Chunk {i+1}/{chunks}: placing {per}")
        order = client.place_order(
            symbol=symbol,
            side=side,
            order_type='LIMIT',
            quantity=per,
            price=price,
            timeInForce=tif
        )
        results.append(order)
        if i < chunks - 1:
            time.sleep(interval_seconds)
    logger.info("TWAP complete")
    return results
