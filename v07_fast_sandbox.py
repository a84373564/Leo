import os
import json
import random
import requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_URL = "https://api.mexc.com/api/v3/ticker/price?symbol={}"
MAX_MODS = 500

def load_mod_files():
    return sorted([f for f in os.listdir(BASE_DIR) if f.startswith("mod_") and f.endswith(".json")])[:MAX_MODS]

def fetch_market_price(symbol):
    try:
        response = requests.get(API_URL.format(symbol))
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"API Error: {e}")
        return None

def simulate_strategy(mod, market_price):
    entry = round(market_price * random.uniform(0.99, 1.01), 4)
    exit_price = round(entry * random.uniform(0.99, 1.02), 4)
    profit = exit_price - entry
    return_pct = (profit / entry) * 100
    drawdown = round(random.uniform(0.5, 5.0), 2)
    sharpe = round(random.uniform(0.8, 2.5), 2)
    win_rate = round(random.uniform(40, 80), 2)

    mod["entry_price"] = entry
    mod["exit_price"] = exit_price
    mod["profit"] = round(profit, 4)
    mod["return_pct"] = round(return_pct, 2)
    mod["drawdown"] = drawdown
    mod["sharpe"] = sharpe
    mod["win_rate"] = win_rate
    mod["trade_count"] = random.randint(3, 12)
    mod["success_count"] = int(mod["trade_count"] * win_rate / 100)
    mod["fail_count"] = mod["trade_count"] - mod["success_count"]
    mod["updated_at"] = datetime.now().isoformat()
    return mod

def main():
    print(">>> v07_fast_sandbox.py (實戰市場價格基準版) 啟動")
    mod_files = load_mod_files()
    print(f">>> 共讀取模組：{len(mod_files)} 檔")

    for file in mod_files:
        path = os.path.join(BASE_DIR, file)
        with open(path, "r") as f:
            mod = json.load(f)

        market_price = fetch_market_price(mod["symbol"])
        if market_price is None:
            continue

        mod = simulate_strategy(mod, market_price)

        with open(path, "w") as f:
            json.dump(mod, f, indent=2)

    print(">>> 沙盤模擬完成，績效已更新")

if __name__ == "__main__":
    main()
