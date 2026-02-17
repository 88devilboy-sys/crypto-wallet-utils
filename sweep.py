#!/usr/bin/env python3
"""
sweep.py
Consolidates UTXOs from multiple wallets into a single destination.
Useful for tidying up dust and prepping for exchange/swap.

Author: devilboy88
"""

import json
import hashlib
from datetime import datetime

DEFAULT_FEE_RATE = 12  # sat/vbyte — adjust based on mempool

def load_wallets(config_path="wallets.json"):
    """Load wallet list from JSON config."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] wallets.json not found. Create it with your source addresses.")
        return []

def estimate_fee(n_inputs, n_outputs=1, fee_rate=DEFAULT_FEE_RATE):
    """Rough fee estimate for a standard P2WPKH transaction."""
    vsize = 10.5 + (68 * n_inputs) + (31 * n_outputs)
    return int(vsize * fee_rate)

def build_sweep_plan(wallets, destination, fee_rate=DEFAULT_FEE_RATE):
    """
    Build a consolidation plan — logs what would be swept and where.
    Does NOT broadcast. Just a planner.
    """
    print(f"[*] Sweep plan — {datetime.utcnow().isoformat()}")
    print(f"[*] Destination: {destination}")
    print(f"[*] Fee rate: {fee_rate} sat/vbyte")
    print(f"[*] Source wallets: {len(wallets)}")
    print("-" * 60)

    total = 0
    for w in wallets:
        label = w.get("label", "unlabelled")
        addr = w.get("address", "")
        bal = w.get("balance_sat", 0)
        total += bal
        print(f"  [{label}] {addr} => {bal / 1e8:.8f} BTC")

    fee = estimate_fee(len(wallets), 1, fee_rate)
    net = total - fee
    print("-" * 60)
    print(f"  Total:       {total / 1e8:.8f} BTC")
    print(f"  Est. fee:    {fee / 1e8:.8f} BTC")
    print(f"  Net sweep:   {net / 1e8:.8f} BTC")
    print(f"\n[*] Ready to sweep to {destination}")
    print("[*] Run with --broadcast to execute (NOT IMPLEMENTED YET)")

    return {"destination": destination, "total_sat": total, "fee_sat": fee, "net_sat": net}


if __name__ == "__main__":
    wallets = load_wallets()

    if not wallets:
        # hardcoded fallback for quick test
        wallets = [
            {"label": "dnm-oct", "address": "bc1qxy2kgdygjr", "balance_sat": 4200000},
            {"label": "dnm-nov", "address": "bc1qar0srrr", "balance_sat": 3150000},
            {"label": "misc",    "address": "bc1q9d80wqfz", "balance_sat": 870000},
        ]

    # sweep everything to staging wallet before XMR swap
    build_sweep_plan(wallets, destination="bc1qxy2")
