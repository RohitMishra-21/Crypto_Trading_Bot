import math
import logging

logger = logging.getLogger(__name__)

class SymbolFilters:
    def __init__(self, lot_step, min_qty, max_qty, price_tick, min_price, max_price, min_notional):
        self.lot_step = float(lot_step)
        self.min_qty = float(min_qty)
        self.max_qty = float(max_qty)
        self.price_tick = float(price_tick)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.min_notional = float(min_notional)

    def round_qty(self, qty: float) -> float:
        return math.floor(qty / self.lot_step) * self.lot_step

    def round_price(self, price: float) -> float:
        # Round down to nearest tick
        return math.floor(price / self.price_tick) * self.price_tick

def extract_filters(symbol_info) -> SymbolFilters:
    if not symbol_info:
        raise ValueError("Symbol not found in exchange info.")
    price_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER')
    lot_filter = next(f for f in symbol_info['filters'] if f['filterType'] in ('LOT_SIZE','MARKET_LOT_SIZE'))
    notional_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL')
    return SymbolFilters(
        lot_step=lot_filter['stepSize'],
        min_qty=lot_filter['minQty'],
        max_qty=lot_filter['maxQty'],
        price_tick=price_filter['tickSize'],
        min_price=price_filter['minPrice'],
        max_price=price_filter['maxPrice'],
        min_notional=notional_filter['notional']
    )

def validate_side(side: str):
    s = side.upper()
    if s not in ('BUY','SELL'):
        raise ValueError("side must be BUY or SELL")
    return s

def validate_order_type(order_type: str):
    t = order_type.upper()
    allowed = {'MARKET','LIMIT','STOP_LIMIT','TWAP', 'OCO'}
    if t not in allowed:
        raise ValueError(f"order_type must be one of {allowed}")
    return t

def validate_and_normalize(client, symbol: str, side: str, order_type: str, quantity: float, price: float=None, stop_price: float=None, stop_limit_price: float=None):
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    si = client.symbol_info(symbol)
    filters = extract_filters(si)

    if quantity <= 0:
        raise ValueError("quantity must be > 0")
    qty_rounded = round(filters.round_qty(quantity), 8)
    if qty_rounded < filters.min_qty:
        raise ValueError(f"quantity too small. min {filters.min_qty}")
    if qty_rounded > filters.max_qty:
        raise ValueError(f"quantity too large. max {filters.max_qty}")

    price_rounded = None
    stop_rounded = None
    stop_limit_rounded = None
    if order_type in ('LIMIT','STOP_LIMIT','TWAP', 'OCO'):
        if price is None or price <= 0:
            raise ValueError("price must be > 0 for this order type")
        price_rounded = round(filters.round_price(price), 8)
        # Bounds check (Binance may still accept out-of-range due to filters updates)
        if price_rounded < filters.min_price or price_rounded > filters.max_price:
            logger.warning("price outside advertised bounds; proceeding but Binance may reject.")
        if qty_rounded * price_rounded < filters.min_notional:
            raise ValueError(f"Notional value (qty * price) is too small. min {filters.min_notional}")

    if order_type in ('STOP_LIMIT', 'OCO'):
        if stop_price is None or stop_price <= 0:
            raise ValueError("stop_price must be > 0 for this order type")
        stop_rounded = round(filters.round_price(stop_price), 8)

    if order_type == 'OCO':
        if stop_limit_price is None or stop_limit_price <= 0:
            raise ValueError("stop_limit_price must be > 0 for OCO orders")
        stop_limit_rounded = round(filters.round_price(stop_limit_price), 8)

    return qty_rounded, price_rounded, stop_rounded, stop_limit_rounded
