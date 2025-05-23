import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "mexc_api_config.json")
SYMBOL_POOL_PATH = os.path.join(BASE_DIR, "symbol_pool.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "capital_plan.json")

MIN_CAPITAL_PER_SYMBOL = 15     # 每幣至少分到多少才會納入
FEE_BUFFER = 0.5                # 預留手續費

def load_keys():
    with open(CONFIG_PATH, "r") as f:
        c = json.load(f)
    return c["access_key"], c["secret_key"]

def fetch_wallet_usdt(api_key):
    url = "https://api.mexc.com/api/v3/account"
    headers = {"X-MEXC-APIKEY": api_key}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        balances = res.json()["balances"]
        for b in balances:
            if b["asset"] == "USDT":
                return float(b["free"])
    except:
        print("[ERROR] 無法取得錢包餘額")
    return 0.0

def load_symbol_pool():
    with open(SYMBOL_POOL_PATH, "r") as f:
        return json.load(f)

def allocate(usdt_balance, symbols):
    usable = usdt_balance - FEE_BUFFER
    if usable <= 0 or not symbols:
        return {}

    max_slots = len(symbols)
    raw_share = usable / max_slots
    selected = [s for s in symbols if raw_share >= MIN_CAPITAL_PER_SYMBOL]

    if not selected:
        print("[WARNING] 沒有任何幣可安全分資")
        return {}

    final_share = usable / len(selected)
    plan = {s: round(final_share, 3) for s in selected}
    return plan

def main():
    print(">>> v05_capital_allocator.py 啟動（實戰最賺錢版本）")
    api_key, _ = load_keys()
    usdt_balance = fetch_wallet_usdt(api_key)
    print(f">>> 錢包 USDT 可用：{usdt_balance:.2f}（含預留）")

    symbols = load_symbol_pool()
    plan = allocate(usdt_balance, symbols)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(plan, f, indent=2)

    print(f">>> 配資完成，共 {len(plan)} 幣，已輸出至 capital_plan.json")

if __name__ == "__main__":
    main()
