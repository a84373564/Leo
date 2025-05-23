import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KING_FILE = os.path.join(BASE_DIR, "king_pool.json")
MEMORY_FILE = os.path.join(BASE_DIR, "memory_bank.json")

def load_king():
    with open(KING_FILE, "r") as f:
        return json.load(f)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def main():
    print(">>> mod_slayer.py 啟動（模組淘汰器）")
    king = load_king()
    king_file = king.get("_file")
    memory = load_memory()

    killed = 0
    for file in os.listdir(BASE_DIR):
        if file.startswith("mod_") and file.endswith(".json") and file != king_file:
            path = os.path.join(BASE_DIR, file)
            try:
                with open(path, "r") as f:
                    mod = json.load(f)
                memory.append({
                    "symbol": mod.get("symbol"),
                    "strategy": mod.get("strategy"),
                    "score": mod.get("score", 0),
                    "death_reason": "淘汰（非王者）",
                    "killed_at": datetime.now().isoformat()
                })
            except:
                pass
            os.remove(path)
            killed += 1

    save_memory(memory)
    print(f">>> 已淘汰 {killed} 個模組，只留下王者 {king_file}")

if __name__ == "__main__":
    main()
