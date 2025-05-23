import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "symbol_blacklist.json")

MIN_PRICE = 0.002
MIN_VOLUME = 1_000_000
MIN_VOLATILITY = 0.003
BAN_KEYWORDS = ["SHIT", "PEPE", "LADY", "SATS", "1000", "INU"]

def fetch_market_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise Exception(f"API 請求失敗：{resp.status_code}")
    return resp.json()

def is_blacklisted(item):
    symbol = item.get("symbol", "")
    if not symbol.endswith("USDT"):
        return True

    quote_vol = float(item.get("quoteVolume", 0))
    high = float(item.get("highPrice", 0))
    low = float(item.get("lowPrice", 0))
    last_price = float(item.get("lastPrice", 0))

    if quote_vol < MIN_VOLUME:
        return True
    if last_price < MIN_PRICE:
        return True
    if high == 0 or low == 0:
        return True
    if (high - low) / high < MIN_VOLATILITY:
        return True
    for ban_word in BAN_KEYWORDS:
        if ban_word in symbol.upper():
            return True

    return False

def main():
    print(">>> v03.5 自動黑名單生成器啟動")
    data = fetch_market_data()
    blacklist = []

    for item in data:
        symbol = item.get("symbol", "")
        if is_blacklisted(item):
            blacklist.append(symbol)

    with open(OUTPUT_PATH, "w") as f:
        json.dump({"symbols": blacklist}, f, indent=2)

    print(f">>> 黑名單共 {len(blacklist)} 檔，已寫入 symbol_blacklist.json")

if __name__ == "__main__":
    main()
