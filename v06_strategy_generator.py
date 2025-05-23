import json
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "system_schema.json")
SYMBOL_POOL_PATH = os.path.join(BASE_DIR, "symbol_pool.json")
TOTAL_MOD_COUNT = 500
STRATEGY_TYPES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def load_symbols():
    with open(SYMBOL_POOL_PATH, "r") as f:
        return json.load(f)

def generate_strategy_config(symbol, strategy_type, index, schema):
    mod = dict(schema)
    mod["symbol"] = symbol
    mod["strategy"] = f"{strategy_type}-{index+1}"
    mod["capital"] = 0
    mod["created_at"] = datetime.now().isoformat()
    mod["updated_at"] = mod["created_at"]
    mod["is_king"] = False
    mod["is_elite"] = False
    mod["lineage"] = ""
    mod["from_retry"] = False
    mod["score"] = 0
    mod["notes"] = "自動生成模組"
    return mod

def main():
    print(">>> v06_strategy_generator.py 啟動（500 模組廝殺制）")
    schema = load_schema()
    symbols = load_symbols()
    symbol_count = len(symbols)

    if symbol_count == 0:
        print("[ERROR] 幣池為空，無法生成")
        return

    per_symbol = TOTAL_MOD_COUNT // symbol_count
    remainder = TOTAL_MOD_COUNT % symbol_count

    count = 0
    for idx, symbol in enumerate(symbols):
        this_symbol_count = per_symbol + (1 if idx < remainder else 0)
        generated = 0
        attempts = 0

        while generated < this_symbol_count and attempts < 10000:
            s_type = random.choice(STRATEGY_TYPES)
            s_index = random.randint(1, 99)
            name = f"mod_{symbol.lower()}_{s_type}-{s_index:02d}.json"
            path = os.path.join(BASE_DIR, name)
            if os.path.exists(path):
                attempts += 1
                continue

            mod = generate_strategy_config(symbol, s_type, s_index, schema)
            with open(path, "w") as f:
                json.dump(mod, f, indent=2)
            generated += 1
            count += 1

    print(f">>> 共生成模組：{count} 檔，完成！")

if __name__ == "__main__":
    main()
