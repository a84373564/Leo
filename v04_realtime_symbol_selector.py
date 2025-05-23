import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "symbol_pool.json")
BLACKLIST_PATH = os.path.join(BASE_DIR, "symbol_blacklist.json")

MAX_SYMBOLS = 2
MIN_CAPITAL_PER_SYMBOL = 35  # 每幣最低操作資金（USDT）
VOLUME_THRESHOLD = 2000000   # 最低成交量
VOLATILITY_THRESHOLD = 0.01  # 最低波動率（1%）

def load_blacklist():
    if os.path.exists(BLACKLIST_PATH):
        with open(BLACKLIST_PATH, "r") as f:
            return set(json.load(f).get("symbols", []))
    return set()

def fetch_market_data():
    url = "https://api.mexc.com/api/v3/ticker/24hr"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise Exception(f"API 請求失敗：{resp.status_code}")
    return resp.json()

def filter_and_rank_symbols(data, blacklist):
    candidates = []
    for item in data:
        symbol = item.get("symbol", "")
        if not symbol.endswith("USDT") or symbol in blacklist:
            continue

        volume = float(item.get("quoteVolume", 0))
        high = float(item.get("highPrice", 0))
        low = float(item.get("lowPrice", 0))

        if volume < VOLUME_THRESHOLD or high == 0 or low == 0:
            continue

        volatility = (high - low) / high
        if volatility < VOLATILITY_THRESHOLD:
            continue

        # 預設模擬你有 MIN_CAPITAL_PER_SYMBOL，要能實際買入
        price = float(item.get("lastPrice", 0))
        if price == 0 or (MIN_CAPITAL_PER_SYMBOL / price) < 1e-6:
            continue  # 太小單位買不到

        score = volume * volatility  # 綜合強度
        candidates.append((symbol, score))

    candidates.sort(key=lambda x: -x[1])
    return [s[0] for s in candidates[:MAX_SYMBOLS]]

def main():
    print(">>> v03 強化版：實戰熱門幣選擇器 啟動")
    blacklist = load_blacklist()
    data = fetch_market_data()
    selected = filter_and_rank_symbols(data, blacklist)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(selected, f, indent=2)

    print(f">>> 最終選出 {len(selected)} 檔活躍幣：{selected}")
    print(f">>> 已寫入：{OUTPUT_PATH}")

if __name__ == "__main__":
    main()
