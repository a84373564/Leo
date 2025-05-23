import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KING_FILE = os.path.join(BASE_DIR, "king_pool.json")

def load_mods():
    files = [f for f in os.listdir(BASE_DIR) if f.startswith("mod_") and f.endswith(".json")]
    mods = []
    for f in files:
        path = os.path.join(BASE_DIR, f)
        with open(path, "r") as fp:
            mod = json.load(fp)
            mod["_file"] = f
            mods.append(mod)
    return mods

def main():
    print(">>> v09_mod_king_selector.py 啟動（唯一王者選拔）")
    mods = load_mods()
    if not mods:
        print("[ERROR] 找不到任何模組")
        return

    best = sorted(mods, key=lambda x: x.get("score", 0), reverse=True)[0]
    now = datetime.now().isoformat()
    best["is_king"] = True
    best["crowned_at"] = now
    best["king_count"] = best.get("king_count", 0) + 1
    best["survival_rounds"] = 0
    best["king_score"] = best.get("score", 0)

    with open(KING_FILE, "w") as f:
        json.dump(best, f, indent=2)
    print(f">>> 王者模組：{best['_file']}  分數：{best.get('score')}")
    print(f">>> 已寫入：{KING_FILE}")

    # 殺掉其餘模組
    for mod in mods:
        if mod["_file"] != best["_file"]:
            os.remove(os.path.join(BASE_DIR, mod["_file"]))
    print(">>> 其餘模組已全部刪除")

if __name__ == "__main__":
    main()
