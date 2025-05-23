import requests
import time
import hashlib
import hmac
import json
import os
from urllib.parse import urlencode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "mexc_api_config.json")
SYMBOL_POOL_PATH = os.path.join(BASE_DIR, "symbol_pool.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "capital_plan.json")

MIN_CAPITAL_PER_SYMBOL = 15
FEE_BUFFER = 0.5

def load_keys():
    with open(CONFIG_PATH, "r") as f:
        c = json.load(f)
    return c["access_key"], c["secret_key"]

def signed_request(api_key, secret_key, endpoint):
    url = f"https://api.mexc.com{endpoint}"
    timestamp = int(time.time() * 1000)
    query = {"timestamp": timestamp}
    query_string = urlencode(query)
    signature = hmac.new(
        secret_key.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()
    full_url = f"{url}?{query_string}&signature={signature}"
    headers = {"X-MEXC-APIKEY": api_key}
    r = requests.get(full_url, headers=headers, timeout=10)
    return r.json()

def fetch_wallet_usdt(api_key, secret_key):
    try:
        data = signed_request(api_key, secret_key, "/api/v3/account")
        balances = data.get("balances", [])
        for b in balances:
            if b["asset"] == "USDT":
                return float(b.get("free", 0))
    except Exception as e:
        print(f"[ERROR] 無法取得餘額: {str(e)}")
    return 0.0

def load_symbol_pool():
    with open(SYMBOL_POOL_PATH, "r") as f:
        return json.load(f)

def allocate(usdt_balance, symbols):
    usable = usdt_balance - FEE_BUFFER
    if usable <= 0 or not symbols:
        return {}

    raw_share = usable / len(symbols)
    selected = [s for s in symbols if raw_share >= MIN_CAPITAL_PER_SYMBOL]
    if not selected:
        return {}

    final_share = usable / len(selected)
    return {s: round(final_share, 3) for s in selected}

def main():
    print(">>> v05_capital_allocator_signed.py 啟動（含簽名）")
    api_key, secret_key = load_keys()
    usdt_balance = fetch_wallet_usdt(api_key, secret_key)
    print(f">>> 查詢成功，錢包 USDT 可用：{usdt_balance:.2f}")

    symbols = load_symbol_pool()
    plan = allocate(usdt_balance, symbols)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(plan, f, indent=2)

    print(f">>> 配資完成，共 {len(plan)} 檔，已寫入 capital_plan.json")

if __name__ == "__main__":
    main()
