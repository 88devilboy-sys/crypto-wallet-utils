# crypto-wallet-utils

Personal scripts for managing BTC wallets. Nothing fancy — just saves me opening a block explorer every time.

## Scripts

### `wallet_monitor.py`
Polls one or more BTC addresses via the blockchain.info API and logs balances to CSV. Set your addresses in the script or (eventually) a config file.

### `sweep.py`
Plans a UTXO consolidation sweep from multiple source wallets into one destination. Estimates fees based on current sat/vbyte rate. Doesn't broadcast — just a planner for now.

## Setup

```bash
pip install requests
```

## Usage

```bash
# monitor balances every 10 min
python3 wallet_monitor.py

# plan a sweep (edit wallets.json or use hardcoded defaults)
python3 sweep.py
```

## TODO

- [ ] Move wallet addresses to `wallets.json` config (stop hardcoding them lol)
- [ ] Add XMR destination support for post-swap tracking
- [ ] Telegram alerts when balance changes
- [ ] Fee estimation from mempool.space API instead of hardcoded rate
- [ ] Add support for Cake Wallet RPC

## Notes

Built for personal use. Not production code. Don't @ me.
