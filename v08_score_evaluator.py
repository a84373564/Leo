import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_MODS = 500

def load_mods():
    files = sorted([f for f in os.listdir(BASE_DIR) if f.startswith("mod_") and f.endswith(".json")])[:MAX_MODS]
    mods = []
    for f in files:
        path = os.path.join(BASE_DIR, f)
        with open(path, "r") as fp:
            mod = json.load(fp)
            mod["_filename"] = f
            mods.append(mod)
    return mods

def compute_score(mod):
    r = mod.get("return_pct", 0)
    s = mod.get("sharpe", 0)
    w = mod.get("win_rate", 0)
    d = mod.get("drawdown", 0)
    score = (r * 2) + (s * 10) + (w * 0.5) - (d * 1.5)
    return round(score, 4)

def main():
    print(">>> v08_score_evaluator.py 啟動（模組評分器）")
    mods = load_mods()
    print(f">>> 共載入模組：{len(mods)} 檔")

    for mod in mods:
        mod["score"] = compute_score(mod)

    mods = sorted(mods, key=lambda x: x["score"], reverse=True)

    for i, mod in enumerate(mods):
        mod["score_rank"] = i + 1
        with open(os.path.join(BASE_DIR, mod["_filename"]), "w") as f:
            json.dump(mod, f, indent=2)

    print(">>> 評分完成，模組已排序與更新 score + score_rank")

if __name__ == "__main__":
    main()
