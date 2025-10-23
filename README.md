# Binance Futures Trading Bot (Testnet)

CLI bot for **USDT-M Futures** on Binance Testnet.
Supports **MARKET**, **LIMIT**, **STOP_LIMIT** (bonus) and **TWAP** (bonus).

## Quickstart
1) Register on Testnet: https://testnet.binancefuture.com
2) Create API keys (Futures enabled). Fund with Faucet (test USDT).
3) Install deps:
```bash
pip install -r requirements.txt
```
4) Create `.env` from `.env.example` and fill keys.
5) Run a market order:
```bash
python src/bot.py BTCUSDT BUY MARKET 0.001
```

## Examples
```bash
# Market BUY 0.001 BTC
python src/bot.py BTCUSDT BUY MARKET 0.001

# Limit BUY 0.001 BTC at 40000
python src/bot.py BTCUSDT BUY LIMIT 0.001 --price 40000

# Stop-Limit SELL 0.001 BTC if stop@35000 then limit@34900
python src/bot.py BTCUSDT SELL STOP_LIMIT 0.001 --price 34900 --stop-price 35000

# TWAP: BUY total 0.01 BTC, split into 5 chunks every 30s at limit 38000
python src/bot.py BTCUSDT BUY TWAP 0.01 --price 38000 --chunks 5 --interval 30
```

## Logs
- All actions written to `logs/bot.log` with timestamps and error traces.

## Notes
- For **Futures Testnet**, we override python-binance futures base URL to `https://testnet.binancefuture.com/fapi`.
- OCO is not natively supported on UM Futures; you can emulate via paired TP/SL reduce-only orders and a watcher.
