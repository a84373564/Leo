import os
import json
import requests
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KING_FILE = os.path.join(BASE_DIR, "king_pool.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "realistic_verification.json")
API_URL = "https://api.mexc.com/api/v3/ticker/24hr?symbol={}"

def load_king():
    with open(KING_FILE, "r") as f:
        return json.load(f)

def fetch_real_market_data(symbol):
    try:
        response = requests.get(API_URL.format(symbol))
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def verify_performance(king, market_data):
    sim_price = king.get("exit_price", 0)
    market_price = float(market_data["lastPrice"])
    price_diff = abs(sim_price - market_price) / market_price * 100

    passed = price_diff < 1.0  # 容忍度設定 1%

    return {
        "symbol": king["symbol"],
        "strategy": king["strategy"],
        "simulated_price": sim_price,
        "market_price": market_price,
        "price_diff_pct": round(price_diff, 2),
        "verified_at": datetime.now().isoformat(),
        "passed": passed,
        "alert": None if passed else "模擬與市場價格差異超過1%"
    }

def main():
    print(">>> v12_realistic_verifier.py（實戰最賺錢版本）啟動")
    king = load_king()
    symbol = king.get("symbol", "")
    market_data = fetch_real_market_data(symbol)

    if market_data is None:
        print("[ERROR] 無法取得市場數據")
        return

    result = verify_performance(king, market_data)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f">>> 真實績效驗證完成：{OUTPUT_FILE}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
