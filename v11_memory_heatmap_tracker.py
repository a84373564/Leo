import os
import json
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "memory_bank.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "memory_hotspot.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def analyze(memory):
    symbol_count = Counter()
    strategy_count = Counter()
    missing_field_count = Counter()

    for m in memory:
        symbol = m.get("symbol", "UNKNOWN")
        strategy = m.get("strategy", "UNKNOWN")
        symbol_count[symbol] += 1
        strategy_count[strategy] += 1

        for key in ["score", "return_pct", "sharpe", "drawdown", "win_rate"]:
            if key not in m:
                missing_field_count[key] += 1

    return {
        "top_dead_symbols": symbol_count.most_common(10),
        "top_dead_strategies": strategy_count.most_common(10),
        "top_missing_fields": missing_field_count.most_common(10)
    }

def save_report(report):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)

def main():
    print(">>> v11_memory_heatmap_tracker.py 啟動（死亡熱點統計）")
    memory = load_memory()
    if not memory:
        print("[警告] 記憶庫為空")
        return
    report = analyze(memory)
    save_report(report)
    print(f">>> 死亡熱點已輸出：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
