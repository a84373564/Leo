import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KING_FILE = os.path.join(BASE_DIR, "king_pool.json")
ARCHIVE_FILE = os.path.join(BASE_DIR, "elite_archive.json")

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print(">>> v10_elite_archive.py 啟動（歷代封神榜）")
    if not os.path.exists(KING_FILE):
        print("[ERROR] 找不到 king_pool.json")
        return

    with open(KING_FILE, "r") as f:
        king = json.load(f)

    if not king.get("is_king", False):
        print("[ERROR] king_pool.json 並非王者資料")
        return

    archive = load_json(ARCHIVE_FILE)

    # 防重複封存
    exists = any(k["_file"] == king.get("_file") for k in archive)
    if exists:
        print(f">>> 王者 {king.get('_file')} 已存在封神榜，略過寫入")
        return

    archive.append(king)
    save_json(ARCHIVE_FILE, archive)

    print(f">>> 王者 {king.get('_file')} 已成功封神，共 {len(archive)} 位歷代王者")

if __name__ == "__main__":
    main()
