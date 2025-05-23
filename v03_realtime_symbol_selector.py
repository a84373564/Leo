import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKER_FILE = os.path.join(BASE_DIR, "tickers.json")
BLACKLIST_FILE = os.path.join(BASE_DIR, "symbol_blacklist.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "symbol_pool.json")

VOLUME_THRESHOLD = 5000000  # USDT
VOLATILITY_THRESHOLD = 0.01  # 1%

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def select_symbols():
    tickers = load_json(TICKER_FILE)
    blacklist = load_json(BLACKLIST_FILE).get("symbols", [])
    selected = []

    for symbol, info in tickers.items():
        vol = info.get("volume_usdt", 0)
        high = info.get("high", 1)
        low = info.get("low", 1)
        if symbol in blacklist:
            continue
        if vol >= VOLUME_THRESHOLD and (high - low) / high >= VOLATILITY_THRESHOLD:
            selected.append(symbol)

    save_json(OUTPUT_FILE, selected)
    print(f">>> 已選出 {len(selected)} 檔活躍幣種，儲存於：{OUTPUT_FILE}")

if __name__ == "__main__":
    select_symbols()
