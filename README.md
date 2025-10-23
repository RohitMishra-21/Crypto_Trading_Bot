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
1. Basic Orders

  Place a MARKET Order
  This command will place a simple market order to buy 0.01 BTCUSDT.

  Command:
   1 python -m src.bot BTCUSDT BUY MARKET 0.01
  Expected Outcome: A new market order will be placed and likely filled immediately. The bot will print the order confirmation from the exchange.

  Place a LIMIT Order
  This command will place a limit order to sell 0.01 BTCUSDT at a price of $90,000.

  Command:

   1 python -m src.bot BTCUSDT SELL LIMIT 0.01 --price 103628.70
  Expected Outcome: A new limit order will be placed. Since the price is likely above the current market price, the order will remain open until
  the market price reaches the limit price.

  2. Advanced Orders

  Place a STOP-LIMIT Order
  This command places a stop-limit order to sell 0.01 BTCUSDT. If the price drops to $60,000, a limit order will be placed to sell at $59,950.

  Command:
   1 python -m src.bot BTCUSDT SELL STOP_LIMIT 0.01 --price 59950 --stop-price 60000
  Expected Outcome: A new stop-limit order will be created. This is a powerful tool for managing risk.

  Place a TWAP (Time-Weighted Average Price) Order
  This command demonstrates the TWAP functionality by splitting a larger order into smaller chunks. It will buy a total of 0.03 BTCUSDT in 3
  separate orders of 0.01 BTC each, placed 10 seconds apart.

  Command:
   1 python -m src.bot BTCUSDT BUY TWAP 0.03 --price 60000 --chunks 3 --interval 10
  Expected Outcome: The bot will place three separate limit orders, one every 10 seconds. This is useful for reducing the market impact of large
  orders.

  Place an OCO (One-Cancels-the-Other) Order
  This command showcases the OCO order type, which is excellent for setting a take-profit and a stop-loss at the same time.

  Command:

   1 python -m src.bot BTCUSDT SELL OCO 0.01 --price 61000 --stop-price 59000 --stop-limit-price 59050
  Expected Outcome: Two orders will be placed. If the price goes up to $61,000, the take-profit order will be filled, and the stop-loss order will
  be canceled. If the price drops to $59,000, the stop-loss order will be triggered, and the take-profit order will be canceled.

  3. Validation System Demonstration

  Minimum Notional Value Validation
  This command will attempt to place an order with a notional value below the exchange's minimum requirement.

  Command:
   1 python -m src.bot BTCUSDT BUY LIMIT 0.001 --price 10
  Expected Outcome: The bot will not send the order to the exchange. Instead, it will immediately raise a ValueError with the message: Notional 
  value (qty * price) is too small. min 100.0. This demonstrates the proactive validation that was added.

  Invalid Input Validation
  This command attempts to place an order with an invalid side.

  Command:
   1 python -m src.bot BTCUSDT INVALID_SIDE MARKET 0.01
  Expected Outcome: The bot will raise a ValueError with the message: side must be BUY or SELL, demonstrating the built-in input validation.

  By running these commands, you can effectively demonstrate the full range of the bot's capabilities, from basic order placement to advanced                    
  trading strategies and robust error handling.

## Logs
- All actions written to `logs/bot.log` with timestamps and error traces.

## Notes
- For **Futures Testnet**, we override python-binance futures base URL to `https://testnet.binancefuture.com/fapi`.
- OCO is not natively supported on UM Futures; you can emulate via paired TP/SL reduce-only orders and a watcher.